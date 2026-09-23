import pyrealsense2 as rs
import numpy as np
import cv2
import time
from interbotix_xs_modules.arm import InterbotixManipulatorXS
from origin_realsense import find_origin
from ultralytics import YOLO
from ultralytics.utils.plotting import Annotator
from arm_movement import pick_up
def get_position():
    bot = InterbotixManipulatorXS("vx300s", "arm", "gripper")
    # Configure depth and color streams
    pipeline = rs.pipeline()
    config = rs.config()
    model = YOLO('best_data.pt')
    # Get device product line for setting a supporting resolution
    pipeline_wrapper = rs.pipeline_wrapper(pipeline)

    config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
    config.enable_stream(rs.stream.color, 1920, 1080, rs.format.bgr8, 6)

    bot.arm.go_to_home_pose()
    bot.arm.set_ee_cartesian_trajectory(x=-0.2)
    bot.arm.set_ee_cartesian_trajectory(pitch=1.3)
    time.sleep(2)
    # Start streaming
    pipeline.start(config)
    #start_time = time.time()
    count=0
    y= []
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
            if count ==20:
            #out=find_origin(color_image)
            #print(out)
                results = model.predict(color_image)

                for r in results:
                    
                    annotator = Annotator(color_image)
                    
                    boxes = r.boxes
                    for box in boxes:
                        
                        b = box.xyxy[0] 
                        #print(b)# get box coordinates in (left, top, right, bottom) format
                        left = int(b[0])
                        top = int(b[1])
                        right = int(b[2])
                        bottom = int(b[3])
                        cX = int((left+right) / 2.0)
                        cY = int((top + bottom) / 2.0)
                        center = (cX,cY)
                        y.append(center)
                        c = box.cls
                        annotator.box_label(b, model.names[int(c)])
                bot.arm.go_to_sleep_pose()    
                img = annotator.result()
                print(y[0])
                cv2.circle(img, y[0], 4, (0, 0, 255), -1)
                cv2.imwrite("images/img1.png",img)  
                center = find_origin(color_image)
                print(center)
                xin = ((y[0][0]*0.0386)-27)/100
                yin = ((y[0][1]*0.0386)+17)/100
                print(round(xin,2),round(yin,2))
                pick_up(round(yin,2),round(xin,2))

                break
            key = cv2.waitKey(1) & 0xFF
            # if the 'q' key is pressed, stop the loop

    finally:
        bot.arm.go_to_sleep_pose()    

        pipeline.stop()
if __name__ == "__main__":
    get_position()