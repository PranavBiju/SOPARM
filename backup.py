from interbotix_xs_modules.arm import InterbotixManipulatorXS
import numpy as np
import pyrealsense2 as rs
from pathlib import Path
import glob
import time
import cv2
from imutils.perspective import four_point_transform
from name_meds import name_meds
def identify_new():
    bot = InterbotixManipulatorXS("vx300s", "arm", "gripper")
    bot.gripper.open()
    #pick up unkown bottle from a defined location
    bot.arm.set_ee_pose_components(x=0.3, z=0.2)
    bot.arm.set_ee_cartesian_trajectory(z=-0.12)
    bot.arm.set_single_joint_position("waist", -np.pi/15)
    bot.arm.set_ee_cartesian_trajectory(x=0.15)
    bot.gripper.close()
    time.sleep(1)
    bot.arm.set_ee_cartesian_trajectory(x=-0.15)
    #put it on the rotating platform
    bot.arm.set_ee_cartesian_trajectory(z=0.12)
    bot.arm.set_single_joint_position("waist", -np.pi/6)
    bot.arm.set_ee_cartesian_trajectory( x=0.135,z=-0.04)
    bot.gripper.open()
    bot.arm.set_ee_cartesian_trajectory( x=-0.135,z=0.04)
    bot.gripper.close()
    time.sleep(1)
    #adjust camera position for image capture for panorama
    bot.arm.set_ee_cartesian_trajectory(x=0.025,z=-0.12)

    # Configure depth and color streams
    pipeline = rs.pipeline()
    config = rs.config()
    pipeline_wrapper = rs.pipeline_wrapper(pipeline)
    pipeline_profile = config.resolve(pipeline_wrapper)
    config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
    config.enable_stream(rs.stream.color, 1920, 1080, rs.format.bgr8, 6)


    try:
        # Start streaming
        pipeline.start(config)
        start_time = time.time()
        count=0
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
            key= cv2.waitKey(1) & 0xFF
            # if the 'q' key is pressed, stop the loop
            if count>10 and count%8 ==0:
                name = "images/panorama_images/img" + str(count)+".png"
                cv2.imwrite(name,color_image) 
            if key == ord("q"):
                pipeline.stop()
                break
            if time.time()-start_time >15:
                pipeline.stop()
                break   
        cv2.destroyAllWindows()  
        bot.arm.set_ee_cartesian_trajectory(x=-0.025,z=0.12)
        bot.gripper.open()
        bot.arm.set_ee_cartesian_trajectory( x=0.135,z=-0.04)
        bot.gripper.close()
        time.sleep(1)
        bot.arm.set_ee_cartesian_trajectory( x=-0.135,z=0.04)

        bot.arm.set_single_joint_position("waist", 0)
        bot.arm.go_to_home_pose()
        bot.arm.go_to_sleep_pose()
        images = glob.glob('images/panorama_images/*.png')
        image_paths=[str(p) for p in images] 
        # initialized a list of images 
        imgs = [] 
        pts = np.array([(1000,536),(1000,150),(1240,150),(1240,536)])
        print(len(image_paths))
        for i in range(len(image_paths)): 
            image = cv2.imread(image_paths[i])
            image = four_point_transform(image, pts)
            imgs.append(image) 

        cv2.imwrite('images/1.png',imgs[0]) 
        cv2.imwrite('images/2.png',imgs[1]) 
        cv2.imwrite('images/3.png',imgs[2]) 

        stitchy=cv2.Stitcher.create() 
        (dummy,output)=stitchy.stitch(imgs) 

        if dummy != cv2.STITCHER_OK: 
        # checking if the stitching procedure is successful 
        # .stitch() function returns a true value if stitching is 
        # done successfully 
            print("stitching ain't successful") 
        else: 
            print('Your Panorama is ready!!!') 
            cv2.imwrite('panorama.png',output) 
    finally:
        
        name_meds()

if __name__ == "__main__":
    identify_new()
