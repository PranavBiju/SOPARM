from interbotix_xs_modules.arm import InterbotixManipulatorXS
import numpy as np
import time
def shelf_meds(day):
    bot = InterbotixManipulatorXS("vx300s", "arm", "gripper")
    if day == "Monday":
        bot.arm.set_ee_pose_components(x=0.3, z=0.2)
        bot.arm.set_single_joint_position("waist", np.pi/2.0)
        bot.arm.set_ee_cartesian_trajectory(x=0.2, z=-0.12)
        bot.gripper.open()
        bot.arm.set_ee_cartesian_trajectory(x=-0.2, z=0.12)
        bot.arm.go_to_home_pose()
        bot.arm.go_to_sleep_pose()
    if day == "Tuesday":

        bot.arm.set_ee_pose_components(x=0.3, z=0.2)
        bot.arm.set_single_joint_position("waist", np.pi*0.43)
        bot.arm.set_ee_cartesian_trajectory(x=0.2, z=-0.12)
        bot.gripper.open()
        bot.arm.set_ee_cartesian_trajectory(x=-0.2, z=0.12)
        bot.arm.go_to_home_pose()
        bot.arm.go_to_sleep_pose()
    if day == "Wednesday":
        bot.arm.set_ee_pose_components(x=0.3, z=0.2)
        bot.arm.set_single_joint_position("waist", np.pi*0.35)
        bot.arm.set_ee_cartesian_trajectory(x=0.25, z=-0.12)
        bot.gripper.open()
        bot.arm.set_ee_cartesian_trajectory(x=-0.14,z=0.12)
        bot.gripper.close()
        time.sleep(1)
        bot.arm.go_to_home_pose()
        bot.arm.go_to_sleep_pose()
if __name__ == "__main__":
    day ="Monday"
    shelf_meds(day)
    
