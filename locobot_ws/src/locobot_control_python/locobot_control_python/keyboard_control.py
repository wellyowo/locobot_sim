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

# Key mapping dictionary for the base
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

# --- NEW: Key mapping for the head ---
head_key_mappings = {
    't': ('head_tilt_joint', 1.0),   # Tilt Up
    'g': ('head_tilt_joint', -1.0),  # Tilt Down
    'f': ('head_pan_joint', 1.0),    # Pan Left
    'h': ('head_pan_joint', -1.0),   # Pan Right
}

# --- MODIFIED: Updated instructions ---
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

Head Control:                 Gripper:
   t/g - Tilt Up/Down           - (minus) / = (equals)
   f/h - Pan Left/Right

q - Quit
-------------------------------------------
"""

class KeyboardTeleop(Node):
    def __init__(self):
        super().__init__('keyboard_teleop')

        # --- Parameters ---
        self.base_speed = 0.2
        self.turn_speed = 0.5
        self.arm_joint_increment = 0.1
        self.head_joint_increment = 0.1 # --- NEW ---
        self.gripper_joint_increment = 0.01

        # --- Publishers ---
        self.base_pub = self.create_publisher(Twist, '/locobot/diffdrive_controller/cmd_vel_unstamped', 10)
        self.arm_pub = self.create_publisher(JointTrajectory, '/locobot/arm_controller/joint_trajectory', 10)
        self.gripper_pub = self.create_publisher(JointTrajectory, '/locobot/gripper_controller/joint_trajectory', 10)
        self.head_pub = self.create_publisher(JointTrajectory, '/locobot/camera_controller/joint_trajectory', 10) # --- NEW ---

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
        self.gripper_joint_names = ['gripper']
        self.head_joint_names = ['head_pan_joint', 'head_tilt_joint'] # --- NEW ---

    def joint_state_callback(self, msg):
        if self.current_joint_states is None:
            self.get_logger().info('Received first joint state message. Control is ready.')
        self.current_joint_states = msg

    def send_arm_command(self, joint_index, direction):
        # This function remains unchanged
        if self.current_joint_states is None: return
        traj = JointTrajectory()
        traj.joint_names = self.arm_joint_names
        current_positions = [0.0] * len(self.arm_joint_names)
        for i, name in enumerate(self.arm_joint_names):
            try:
                idx = self.current_joint_states.name.index(name)
                current_positions[i] = self.current_joint_states.position[idx]
            except ValueError:
                self.get_logger().error(f"Joint '{name}' not found.")
                return
        current_positions[joint_index] += self.arm_joint_increment * direction
        point = JointTrajectoryPoint()
        point.positions = current_positions
        point.time_from_start.sec = 1
        traj.points.append(point)
        self.arm_pub.publish(traj)
        
    # --- NEW: Function to send head commands ---
    def send_head_command(self, joint_name, direction):
        if self.current_joint_states is None:
            self.get_logger().warn('Cannot control head yet. No joint states received.')
            return

        traj = JointTrajectory()
        traj.joint_names = self.head_joint_names

        # Get current positions for both pan and tilt
        current_positions = [0.0] * len(self.head_joint_names)
        for i, name in enumerate(self.head_joint_names):
            try:
                idx = self.current_joint_states.name.index(name)
                current_positions[i] = self.current_joint_states.position[idx]
            except ValueError:
                self.get_logger().error(f"Joint '{name}' not found in received joint states.")
                return

        # Modify the target joint (pan or tilt)
        target_joint_index = self.head_joint_names.index(joint_name)
        current_positions[target_joint_index] += self.head_joint_increment * direction

        # Create and publish the trajectory
        point = JointTrajectoryPoint()
        point.positions = current_positions
        point.time_from_start.sec = 1
        traj.points.append(point)
        self.head_pub.publish(traj)

    def send_gripper_command(self, direction):
        # This function remains unchanged
        if self.current_joint_states is None: return
        traj = JointTrajectory()
        traj.joint_names = self.gripper_joint_names
        try:
            idx = self.current_joint_states.name.index('left_finger')
            current_pos = self.current_joint_states.position[idx]
        except ValueError:
            self.get_logger().error(f"Gripper joint 'left_finger' not found.")
            return
        target_pos = current_pos + self.gripper_joint_increment * direction
        point = JointTrajectoryPoint()
        point.positions = [target_pos]
        point.time_from_start.sec = 1
        traj.points.append(point)
        self.gripper_pub.publish(traj)

def get_key(settings):
    # This function remains unchanged
    tty.setraw(sys.stdin.fileno())
    key = sys.stdin.read(1)
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key

def main():
    settings = termios.tcgetattr(sys.stdin)
    rclpy.init()
    teleop_node = KeyboardTeleop()

    print(instructions)
    
    spin_thread = threading.Thread(target=rclpy.spin, args=(teleop_node,))
    spin_thread.start()

    try:
        while rclpy.ok():
            key = get_key(settings)
            
            if key == 'q':
                break

            if key in key_mappings:
                linear_vel, angular_vel = key_mappings[key]
                twist = Twist()
                twist.linear.x = linear_vel * teleop_node.base_speed
                twist.angular.z = angular_vel * teleop_node.turn_speed
                teleop_node.base_pub.publish(twist)

            elif key in arm_key_mappings:
                joint_idx, direction = arm_key_mappings[key]
                if arm_key_mappings[key][0] == 5:
                    teleop_node.send_gripper_command(direction)
                else:
                    teleop_node.send_arm_command(joint_idx, direction)

            # --- NEW: Check for head control keys ---
            elif key in head_key_mappings:
                joint_name, direction = head_key_mappings[key]
                teleop_node.send_head_command(joint_name, direction)

    except Exception as e:
        print(e)
    finally:
        twist = Twist()
        teleop_node.base_pub.publish(twist)
        
        rclpy.shutdown()
        spin_thread.join()
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)

if __name__ == '__main__':
    main()