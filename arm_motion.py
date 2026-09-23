from interbotix_xs_modules.arm import InterbotixManipulatorXS
import math

bot = InterbotixManipulatorXS("vx300s", "arm", "gripper")

bot.arm.go_to_home_pose()
bot.arm.go_to_sleep_pose()

