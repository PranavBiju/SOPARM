from interbotix_xs_modules.arm import InterbotixManipulatorXS
import time

def reset_robot():
    # Initialize the robot
    bot = InterbotixManipulatorXS("vx300s", "arm", "gripper")
    
    # Open the gripper to ensure it's not holding anything
    bot.gripper.open()
    time.sleep(1)

    # Move to the home position
    bot.arm.go_to_sleep_pose()
    time.sleep(1)

    # Optionally, move to sleep position if needed (for shutdown)
    # bot.arm.go_to_sleep_pose()

    # Disable torque (optional for safety/shutdown)
    # bot.arm.disable_torque()
    # bot.gripper.disable_torque()

    print("Robot reset to home position.")

# Run the reset
if __name__ == "__main__":
    reset_robot()
