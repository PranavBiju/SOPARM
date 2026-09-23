from interbotix_xs_modules.arm import InterbotixManipulatorXS
import numpy as np
from pathlib import Path
import glob
import time
import cv2
import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
from imutils.perspective import four_point_transform
from name_meds import name_meds

bridge = CvBridge()
latest_frame = None


def image_callback(msg):
    global latest_frame
    latest_frame = bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')


def identify_new():

    global latest_frame

    bot = InterbotixManipulatorXS("vx300s", "arm", "gripper")
    bot.gripper.open()

    # pick up unknown bottle
    bot.arm.set_ee_pose_components(x=0.3, z=0.2)
    bot.arm.set_ee_cartesian_trajectory(z=-0.12)
    bot.arm.set_single_joint_position("waist", -np.pi/15)
    bot.arm.set_ee_cartesian_trajectory(x=0.15)

    bot.gripper.close()
    time.sleep(1)

    bot.arm.set_ee_cartesian_trajectory(x=-0.15)

    # put it on rotating platform
    bot.arm.set_ee_cartesian_trajectory(z=0.12)
    bot.arm.set_single_joint_position("waist", -np.pi/6)
    bot.arm.set_ee_cartesian_trajectory(x=0.135, z=-0.04)

    bot.gripper.open()

    bot.arm.set_ee_cartesian_trajectory(x=-0.135, z=0.04)

    bot.gripper.close()
    time.sleep(1)

    # adjust camera position
    bot.arm.set_ee_cartesian_trajectory(x=0.025, z=-0.12)

    # ROS camera subscriber
    rospy.Subscriber('/camera/color/image_raw', Image, image_callback)

    try:

        start_time = time.time()
        count = 0

        while not rospy.is_shutdown():

            if latest_frame is None:
                continue

            color_image = latest_frame.copy()
            count += 1

            cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
            cv2.imshow('RealSense', color_image)

            key = cv2.waitKey(1) & 0xFF

            if count > 10 and count % 8 == 0:
                name = "images/panorama_images/img" + str(count) + ".png"
                cv2.imwrite(name, color_image)

            if key == ord("q"):
                break

            if time.time() - start_time > 15:
                break

        cv2.destroyAllWindows()

        bot.arm.set_ee_cartesian_trajectory(x=-0.025, z=0.12)
        bot.gripper.open()

        bot.arm.set_ee_cartesian_trajectory(x=0.135, z=-0.04)
        bot.gripper.close()

        time.sleep(1)

        bot.arm.set_ee_cartesian_trajectory(x=-0.135, z=0.04)

        bot.arm.set_single_joint_position("waist", 0)

        bot.arm.set_ee_pose_components(x=0.3, z=0.2)
        bot.arm.set_single_joint_position("waist", -np.pi/2.0)
        bot.arm.set_ee_cartesian_trajectory(x=0.1, z=-0.12)

        bot.gripper.open()

        bot.arm.set_ee_cartesian_trajectory(x=-0.14, z=0.12)
        bot.gripper.close()
        time.sleep(2)

        bot.arm.set_ee_cartesian_trajectory(pitch=1.25)

        scale_start = time.time()
        while not rospy.is_shutdown():
            if latest_frame is None:
                continue
            color_image = latest_frame.copy()
            cv2.imshow('RealSense', color_image)
            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                break
            if time.time() - scale_start > 3:
                cv2.imwrite("images/img3.png", color_image)
                time.sleep(1)
                break

        bot.arm.set_ee_cartesian_trajectory(pitch=-1.25)

        # Pick bottle back up from scale
        bot.gripper.open()
        bot.arm.set_ee_cartesian_trajectory(x=0.14, z=-0.12)
        bot.gripper.close()
        time.sleep(1)
        bot.arm.set_ee_cartesian_trajectory(x=-0.14, z=0.12)

        # Swing to drop-off position (45 degrees past home)
        bot.arm.set_single_joint_position("waist", np.pi/4)
        bot.arm.set_ee_cartesian_trajectory(x=0.1, z=-0.12)
        bot.gripper.open()
        bot.arm.set_ee_cartesian_trajectory(x=-0.1, z=0.12)
        bot.gripper.close()

        bot.arm.go_to_home_pose()
        bot.arm.go_to_sleep_pose()

        images = glob.glob('images/panorama_images/*.png')
        image_paths = [str(p) for p in images]

        imgs = []

        pts = np.array([(1000, 536), (1000, 150), (1240, 150), (1240, 536)])

        print(len(image_paths))

        for i in range(len(image_paths)):

            image = cv2.imread(image_paths[i])
            image = four_point_transform(image, pts)
            imgs.append(image)

        cv2.imwrite('images/1.png', imgs[0])
        cv2.imwrite('images/2.png', imgs[1])
        cv2.imwrite('images/3.png', imgs[2])

        stitchy = cv2.Stitcher.create()

        (dummy, output) = stitchy.stitch(imgs)

        if dummy != cv2.STITCHER_OK:

            print("stitching ain't successful")

        else:

            print('Your Panorama is ready!!!')
            cv2.imwrite('panorama.png', output)

    finally:

        name_meds()


if __name__ == "__main__":
    identify_new()