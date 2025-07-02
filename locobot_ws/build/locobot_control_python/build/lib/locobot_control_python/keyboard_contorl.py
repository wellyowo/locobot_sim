#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from sensor_msgs.msg import JointState
import sys
import termios
import tty
import threading

# Key mapping dictionary
key_mappings = {
    'w': (1.0, 0.0),  # Forward
    's': (-1.0, 0.0), # Backward
    'a': (0.0, 1.0),  # Rotate Left
    'd': (0.0, -1.0), # Rotate Right
    'x': (0.0, 0.0),  # Stop
}

# Arm joint control mapping
# Format: {key: (joint_index, direction)}
arm_key_mappings = {
    'u': (0, 1.0),   # Waist +
    'j': (0, -1.0),  # Waist -
    'i': (1, 1.0),   # Shoulder +
    'k': (1, -1.0),  # Shoulder -
    'o': (2, 1.0),   # Elbow +
    'l': (2, -1.0),  # Elbow -
    'p': (3, 1.0),   # Wrist Angle +
    ';': (3, -1.0),  # Wrist Angle -
    '[': (4, 1.0),   # Wrist Rotate +
    '\'': (4, -1.0), # Wrist Rotate -
    '-': (5, 1.0),   # Gripper Open
    '=': (5, -1.0),  # Gripper Close
}

# Instructions displayed to the user
instructions = """
-------------------------------------------
        Keyboard Teleop for LoCoBot
-------------------------------------------
Base Movement:                Arm Movement:
   w - Forward                   u/j - Waist
   s - Backward                  i/k - Shoulder
   a - Rotate Left               o/l - Elbow
   d - Rotate Right              p/; - Wrist Angle
   x - Stop Base                 [/] - Wrist Rotate

Gripper:                      - (minus) / = (equals)

q - Quit
-------------------------------------------
"""

class KeyboardTeleop(Node):
    def __init__(self):
        super().__init__('keyboard_teleop')

        # --- Parameters ---
        self.base_speed = 0.2  # m/s
        self.turn_speed = 0.5  # rad/s
        self.arm_joint_increment = 0.1  # rad
        self.gripper_joint_increment = 0.01 # meters

        # --- Publishers ---
        self.base_pub = self.create_publisher(Twist, '/locobot/cmd_vel', 10)
        self.arm_pub = self.create_publisher(JointTrajectory, '/locobot/arm_controller/joint_trajectory', 10)
        self.gripper_pub = self.create_publisher(JointTrajectory, '/locobot/gripper_controller/joint_trajectory', 10)

        # --- Subscriber ---
        self.joint_state_sub = self.create_subscription(
            JointState,
            '/locobot/joint_states',
            self.joint_state_callback,
            10
        )

        # --- State Variables ---
        self.current_joint_states = None
        self.arm_joint_names = ['waist', 'shoulder', 'elbow', 'wrist_angle', 'wrist_rotate']
        self.gripper_joint_names = ['gripper'] # This name may vary depending on your URDF/controllers.yaml

    def joint_state_callback(self, msg):
        if self.current_joint_states is None:
            self.get_logger().info('Received first joint state message. Arm control is ready.')
        self.current_joint_states = msg

    def send_arm_command(self, joint_index, direction):
        if self.current_joint_states is None:
            self.get_logger().warn('Cannot control arm yet. No joint states received.')
            return

        # Create a new trajectory message
        traj = JointTrajectory()
        traj.joint_names = self.arm_joint_names

        # Get current positions from the received joint_states
        current_positions = [0.0] * len(self.arm_joint_names)
        for i, name in enumerate(self.arm_joint_names):
            try:
                idx = self.current_joint_states.name.index(name)
                current_positions[i] = self.current_joint_states.position[idx]
            except ValueError:
                self.get_logger().error(f"Joint '{name}' not found in received joint states.")
                return

        # Modify the target joint
        current_positions[joint_index] += self.arm_joint_increment * direction

        # Create a trajectory point
        point = JointTrajectoryPoint()
        point.positions = current_positions
        point.time_from_start.sec = 1  # Reach the goal in 1 second

        traj.points.append(point)
        self.arm_pub.publish(traj)

    def send_gripper_command(self, direction):
        # This is a simplified gripper control. It may need adjustment based on your specific gripper controller type.
        if self.current_joint_states is None:
            self.get_logger().warn('Cannot control gripper yet. No joint states received.')
            return

        traj = JointTrajectory()
        traj.joint_names = self.gripper_joint_names
        
        # This assumes the 'gripper' joint is a single value.
        # It finds the current position of the first finger and applies the increment.
        try:
            idx = self.current_joint_states.name.index('left_finger') # Using one finger as reference
            current_pos = self.current_joint_states.position[idx]
        except ValueError:
            self.get_logger().error(f"Gripper joint 'left_finger' not found.")
            return

        target_pos = current_pos + self.gripper_joint_increment * direction
        
        point = JointTrajectoryPoint()
        point.positions = [target_pos] # The command is often sent to a single meta-joint
        point.time_from_start.sec = 1

        traj.points.append(point)
        self.gripper_pub.publish(traj)


def get_key(settings):
    # A standard function to get a single keypress from the terminal in Linux
    tty.setraw(sys.stdin.fileno())
    key = sys.stdin.read(1)
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key


def main():
    settings = termios.tcgetattr(sys.stdin)
    rclpy.init()
    teleop_node = KeyboardTeleop()

    print(instructions)
    
    # Spin node in a separate thread
    spin_thread = threading.Thread(target=rclpy.spin, args=(teleop_node,))
    spin_thread.start()

    try:
        while rclpy.ok():
            key = get_key(settings)
            
            if key == 'q':
                break

            # --- Base Control ---
            if key in key_mappings:
                linear_vel, angular_vel = key_mappings[key]
                twist = Twist()
                twist.linear.x = linear_vel * teleop_node.base_speed
                twist.angular.z = angular_vel * teleop_node.turn_speed
                teleop_node.base_pub.publish(twist)

            # --- Arm Control ---
            elif key in arm_key_mappings:
                joint_idx, direction = arm_key_mappings[key]
                # Check if it's the gripper or arm
                if arm_key_mappings[key][0] == 5: # Gripper index
                    teleop_node.send_gripper_command(direction)
                else:
                    teleop_node.send_arm_command(joint_idx, direction)

    except Exception as e:
        print(e)
    finally:
        # Publish a final stop message for the base
        twist = Twist()
        teleop_node.base_pub.publish(twist)
        
        rclpy.shutdown()
        spin_thread.join()
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)


if __name__ == '__main__':
    main()