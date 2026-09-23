from interbotix_xs_modules.arm import InterbotixManipulatorXS
import time

def move_to_pose(x=0.3, y=0.0, z=0.2, roll=0.0, pitch=0.0, yaw=0.0):
    # Initialize the robot
    bot = InterbotixManipulatorXS("vx300s", "arm", "gripper")

    # Move to the specified pose
    bot.arm.set_ee_pose_components(x=x, y=y, z=z, roll=roll, pitch=pitch, yaw=yaw)
    time.sleep(1)

    print(f"Moved to pose: x={x}, y={y}, z={z}, roll={roll}, pitch={pitch}, yaw={yaw}")

# Example usage
if __name__ == "__main__":
    # Replace with your desired coordinates
    move_to_pose(x=0.35, y=0.0, z=0.07)
