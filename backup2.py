import pyrealsense2 as rs
import numpy as np
import cv2
from interbotix_xs_modules.arm import InterbotixManipulatorXS
import time
from digits_func import digit_read
from tts2 import tts
def check_weight():
    bot = InterbotixManipulatorXS("vx300s", "arm", "gripper")

    bot.arm.set_ee_pose_components(x=0.3, z=0.2)
    bot.arm.set_single_joint_position("waist", -np.pi/2.0)
    bot.arm.set_ee_cartesian_trajectory(x=0.1, z=-0.12)
    bot.gripper.open()
    bot.arm.set_ee_cartesian_trajectory(x=-0.14, z=0.12)
    bot.gripper.close()
    time.sleep(2)
    bot.arm.set_ee_cartesian_trajectory(pitch=1.25)

    # Configure depth and color streams
    pipeline = rs.pipeline()
    config = rs.config()
    # Get device product line for setting a supporting resolution
    pipeline_wrapper = rs.pipeline_wrapper(pipeline)
    pipeline_profile = config.resolve(pipeline_wrapper)
    device = pipeline_profile.get_device()

    found_rgb = False
    for s in device.sensors:
        if s.get_info(rs.camera_info.name) == 'RGB Camera':
            found_rgb = True
            break
    if not found_rgb:
        print("The demo requires Depth camera with Color sensor")
        exit(0)

    config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
    config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

    pipeline.start(config)
    start_time = time.time()
    count=0
    try:
        while True:

            # Wait for a coherent pair of frames: depth and color
            frames = pipeline.wait_for_frames()
            color_frame = frames.get_color_frame()
            if not color_frame:
                continue
            count = count+1
            # Convert images to numpy arrays
            color_image = np.asanyarray(color_frame.get_data())
            # Show images
            cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
            cv2.imshow('RealSense', color_image)
            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                break
            if time.time()-start_time >3:
                cv2.imwrite("images/img3.png",color_image)
                time.sleep(1)
                weight = digit_read(color_image)
                try:
                    if int(weight)<20:
                        print("The bottle is almost empty")
                        tts("The bottle is almost empty")
                    else:
                        print("The bottle presently weighs:", weight)
                        text = "The bottle presently weighs:" +weight  +"g"
                        tts(text)
                    break
                except:
                    break

    finally:
        pipeline.stop()
        bot.arm.set_ee_cartesian_trajectory(pitch=-1.25)
        bot.gripper.open()
        bot.arm.set_ee_cartesian_trajectory(x=0.14, z=-0.12)
        bot.gripper.close()
        time.sleep(2)
        bot.arm.set_ee_cartesian_trajectory(x=-0.1, z=0.12)
        bot.arm.go_to_home_pose()
        bot.arm.go_to_sleep_pose()

if __name__ == '__main__':
    check_weight()


