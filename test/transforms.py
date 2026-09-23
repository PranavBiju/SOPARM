#!/usr/bin/env python  
import rospy
import tf
import numpy as np
from tf.transformations import quaternion_matrix, euler_from_quaternion

def get_transform_matrix(listener, from_frame, to_frame):
    try:
        # Wait for the transform to become available
        listener.waitForTransform(from_frame, to_frame, rospy.Time(), rospy.Duration(4.0))

        # Get the latest transform
        (trans, rot) = listener.lookupTransform(from_frame, to_frame, rospy.Time(0))

        # Print translation and rotation
        print(f"\nTranslation (x, y, z): {trans}")
        print(f"Rotation (quaternion x, y, z, w): {rot}")
        
        # Convert quaternion to Euler angles
        roll, pitch, yaw = euler_from_quaternion(rot)
        print(f"Rotation (Euler roll, pitch, yaw): {roll:.4f}, {pitch:.4f}, {yaw:.4f}")

        # Compute the 4x4 transformation matrix
        transform_matrix = quaternion_matrix(rot)
        transform_matrix[0:3, 3] = trans

        print("\nTransformation Matrix (4x4):")
        print(np.array_str(transform_matrix, precision=4, suppress_small=True))

        return transform_matrix

    except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException) as e:
        rospy.logerr(f"TF Error: {e}")
        return None

if __name__ == '__main__':
    rospy.init_node('tf_listener_node')

    listener = tf.TransformListener()

    from_frame = "vx300s/base_link"
    to_frame = "detected_bottle_0"

    rospy.sleep(2.0)  # Give tf buffer time to fill

    matrix = get_transform_matrix(listener, from_frame, to_frame)
