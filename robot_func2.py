from interbotix_xs_modules.arm import InterbotixManipulatorXS
import numpy as np
import pyrealsense2 as rs
from ultralytics import YOLO
from ultralytics.utils.plotting import Annotator
import time
import cv2
def pick_up(x):
    
    bot = InterbotixManipulatorXS("vx300s", "arm", "gripper")
    bot.gripper.open()
    
    bot.arm.set_ee_pose_components(x=0.3, z=0.2)
    bot.arm.set_ee_cartesian_trajectory(z=-0.12)                                               
    if (x==2):
        bot.arm.set_single_joint_position("waist", -np.pi/15)
    
    if (x==3):
        bot.arm.set_single_joint_position("waist", np.pi/15)
    
    bot.arm.set_ee_cartesian_trajectory(x=0.15)
    bot.gripper.close()
    bot.arm.set_ee_cartesian_trajectory(x=-0.15)
    bot.arm.go_to_home_pose()
    bot.arm.go_to_sleep_pose()


def get_position(st):
    # Configure depth and color streams
    pipeline = rs.pipeline()
    config = rs.config()
    model = YOLO('best.pt')
    # Get device product line for setting a supporting resolution
    pipeline_wrapper = rs.pipeline_wrapper(pipeline)
    pipeline_profile = config.resolve(pipeline_wrapper)
    #config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
    config.enable_stream(rs.stream.color, 1280, 720, rs.format.bgr8, 6)
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
            cv2.waitKey(1) & 0xFF

            if count ==15 :

                results = model.predict(color_image)
                

                for r in results:
                    annotator = Annotator(color_image)
                    print(r.names)
                    boxes = r.boxes
                    for box in boxes:
                        
                        b = box.xyxy[0] 
                        print(b) # get box coordinates in (left, top, right, bottom) format
                        c = box.cls
                        annotator.box_label(b, model.names[int(c)])
                        name =model.names[int(c)]
                        print(name)
                    
                img = annotator.result()  
                cv2.imshow('RealSense', img)
                cv2.waitKey(1) & 0xFF

                cv2.imwrite("images/img1.png",img) 
                break
    
    finally:
        pipeline.stop()
    if st== "Codifresh-DX":
        center = 2
    if st== "Vicks Vapour":
        center =1
    if st =="Liv52 Himalaya":
        center = 3
    print(center)
    return center

if __name__ =='__main__':
    center= get_position("Liv52 Himalaya")
    #pick_up(center)
