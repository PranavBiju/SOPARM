import rospy
import numpy as np
import cv2
import time

from sensor_msgs.msg import Image
from cv_bridge import CvBridge

from interbotix_xs_modules.arm import InterbotixManipulatorXS
from digits_func import digit_read
from tts2 import tts

bridge = CvBridge()
latest_frame = None


def image_callback(msg):
    global latest_frame
    latest_frame = bridge.imgmsg_to_cv2(msg, desired_encoding="bgr8")


def check_weight():

    global latest_frame

    rospy.Subscriber("/camera/color/image_raw", Image, image_callback)

    bot = InterbotixManipulatorXS("vx300s", "arm", "gripper")

    bot.arm.set_ee_pose_components(x=0.3, z=0.2)
    bot.arm.set_single_joint_position("waist", -np.pi/2.0)
    bot.arm.set_ee_cartesian_trajectory(x=0.1, z=-0.12)

    bot.gripper.open()

    bot.arm.set_ee_cartesian_trajectory(x=-0.14, z=0.12)
    bot.gripper.close()

    time.sleep(2)

    bot.arm.set_ee_cartesian_trajectory(pitch=1.25)

    start_time = time.time()

    try:

        while not rospy.is_shutdown():

            if latest_frame is None:
                continue

            color_image = latest_frame.copy()

            cv2.imshow("RealSense", color_image)

            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                break

            if time.time() - start_time > 3:

                cv2.imwrite("images/img3.png", color_image)

                time.sleep(1)

                weight = digit_read(color_image)

                try:

                    if int(weight) < 20:
                        print("The bottle is almost empty")
                        tts("The bottle is almost empty")

                    else:
                        print("The bottle presently weighs:", weight)

                        text = "The bottle presently weighs:" + weight + " g"
                        tts(text)

                    break

                except:
                    break

    finally:

        bot.arm.set_ee_cartesian_trajectory(pitch=-1.25)

        bot.gripper.open()

        bot.arm.set_ee_cartesian_trajectory(x=0.14, z=-0.12)

        bot.gripper.close()

        time.sleep(2)

        bot.arm.set_ee_cartesian_trajectory(x=-0.1, z=0.12)

        bot.arm.go_to_home_pose()
        bot.arm.go_to_sleep_pose()

        cv2.destroyAllWindows()


if __name__ == "__main__":
    check_weight()