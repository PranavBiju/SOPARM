from interbotix_xs_modules.arm import InterbotixManipulatorXS
import numpy as np
import pyrealsense2 as rs
import time
import cv2
from shelf_aruco import find_aruco_shelf
def check_shelf():
    #initialize robot object
    bot = InterbotixManipulatorXS("vx300s", "arm", "gripper")
    #setup the streams for colour and depth from the realsense
    pipeline = rs.pipeline()
    config = rs.config()
    config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
    config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

    #get the arm to the required position
    bot.arm.set_ee_pose_components(x=0.3, z=0.2)
    bot.arm.set_single_joint_position("waist", np.pi*0.42)
    bot.arm.set_ee_cartesian_trajectory(x=0.11, z= 0.1)
    bot.arm.set_ee_cartesian_trajectory(pitch=1.25)
    #Start the realsense pipeline
    pipeline.start(config)
    start_time = time.time()
    try:
        while True:

            # Wait for a coherent pair of frames: depth and color
            frames = pipeline.wait_for_frames()
            color_frame = frames.get_color_frame()
            if not color_frame:
                continue
            # Convert images to numpy arrays
            color_image = np.asanyarray(color_frame.get_data())
            # Show images
            cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
            cv2.imshow('RealSense', color_image)
            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                break
            if time.time()-start_time >3:
                #save image
                cv2.imwrite("images/imga.png",color_image)
                #run function to find which slots are empty
                lista = find_aruco_shelf(color_image)
                break
    finally:
        #cleanup
        pipeline.stop()
        bot.arm.go_to_home_pose()
        bot.arm.go_to_sleep_pose()
    return lista

if __name__ == "__main__":
    lista = check_shelf()
    for a in lista:
        print(a)