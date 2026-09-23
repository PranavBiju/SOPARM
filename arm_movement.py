from interbotix_xs_modules.arm import InterbotixManipulatorXS
import math

# This script makes the end-effector perform pick and place tasks
# Note that this script may not work for every arm as it was designed for the vx300
# Make sure to adjust commanded joint positions and poses as necessary
#
# To get started, open a terminal and type 'roslaunch interbotix_xsarm_control xsarm_control.launch robot_model:=vx300

def pick_up(x , y):
    bot = InterbotixManipulatorXS("vx300s", "arm", "gripper")

    yin = math.atan(y/x)-0.2
    xin = math.sqrt((x**2)+ (y**2))-0.05

    print(yin)
    print(xin)
    bot.arm.set_ee_pose_components(x=0.3, z =0.2)
    bot.arm.set_ee_cartesian_trajectory(x=xin-0.3,z=-0.12)
    bot.arm.set_single_joint_position("waist", -yin)
    
    bot.gripper.open()
    bot.arm.set_ee_cartesian_trajectory(x=0.1)
    bot.gripper.close()
    bot.arm.set_ee_cartesian_trajectory(x=-0.1, z=0.12)


def drop_off(xin , yin):
    bot = InterbotixManipulatorXS("vx300s", "arm", "gripper")
    bot.arm.set_ee_pose_components(x=xin, z =0.2)
    bot.arm.set_single_joint_position("waist", yin)
    
    bot.arm.set_ee_cartesian_trajectory(x=0.1, z=-0.12)
    bot.gripper.open()
    bot.arm.set_ee_cartesian_trajectory(x=-0.1, z=0.12)
    bot.gripper.close
    bot.arm.go_to_home_pose()
    bot.arm.go_to_sleep_pose()