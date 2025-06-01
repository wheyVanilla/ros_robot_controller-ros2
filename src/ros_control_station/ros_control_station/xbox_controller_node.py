#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Joy
from ros_robot_controller_msgs.msg import MotorsState, MotorState, PWMServoState, SetPWMServoState
from rclpy.qos import QoSProfile, ReliabilityPolicy
from ctypes import c_uint16 as uint16
from std_srvs.srv import Trigger
import os
import subprocess
from datetime import datetime
from slam_toolbox.srv import SerializePoseGraph


class XboxControlStation(Node):
    def __init__(self):
        super().__init__('xbox_control_station')
        self.get_logger().info("Xbox Control Station Node Initialized")
        
        
        # Create QoS profile for controller
        qos = QoSProfile(
            depth=1,
            reliability=ReliabilityPolicy.BEST_EFFORT
        )
        
        # Load parameters from config.yaml

        #TODO: make those parameters as configurable
        
        # Control parameters
        self.max_speed = 1.5     # Maximum RPS
        
        # Servo parameters
        self.center_pwm = 1500   # Center position (90°)
        self.pwm_range = 1000    # PWM range from center (±1000)
        self.max_turn = 0.45      # Maximum turn range (0.5 = ±45°)
        
        # Create maps directory if it doesn't exist
        self.maps_dir = os.path.expanduser('~/maps')
        try:
            os.makedirs(self.maps_dir, exist_ok=True)
            self.get_logger().info(f"Maps directory created/verified at {self.maps_dir}")
        except Exception as e:
            self.get_logger().error(f"Failed to create maps directory: {str(e)}")
            self.maps_dir = None
        
        # Subscribe to Xbox controller
        self.joy_sub = self.create_subscription(
            Joy,
            '/joy',
            self.joy_callback,
            1
        )
        
        # Publishers
        self.motor_pub = self.create_publisher(
            MotorsState,
            'manual_control/set_motor',
            1
        )
        
        self.servo_pub = self.create_publisher(
            SetPWMServoState,
            'manual_control/pwn_servo_set_state',
            1
        )
        
        # Track X button state
        self.x_button_pressed = False
        
        # Create service client for map serialization
        self.serialize_map_client = self.create_client(
            SerializePoseGraph,
            '/slam_toolbox/serialize_map'
        )
        
        # Wait for service to be available
        while not self.serialize_map_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Serialize map service not available, waiting...')
        
    def map_to_pwm(self, turn_value):
        """Map joystick (-1 to 1) to PWM range (500-2500)"""
        # Limit turn range
        turn_value = max(min(turn_value, self.max_turn), -self.max_turn)
        # turn_value = turn_value*self.max_turn

        # Map to PWM and ensure it's an integer
        pwm = int(self.center_pwm - (turn_value * self.pwm_range))
 

        # Ensure within bounds
        return max(min(pwm, 2500), 500)
        
    def joy_callback(self, msg):
        # Get joystick values
        forward = msg.axes[1]    # Left stick up/down (-1 to 1)
        turn = msg.axes[0]       # Left stick left/right (-1 to 1)
        
        # Motor control (forward/backward)
        speed = forward * self.max_speed
    
        motor_msg = MotorsState()
        motor_msg.data = [
            MotorState(id=1, rps=speed),
            MotorState(id=2, rps=-speed)
        ]
        self.motor_pub.publish(motor_msg)
        
        # Servo control (steering)
        pwm = self.map_to_pwm(turn)
        servo_msg = SetPWMServoState()
        servo_state = PWMServoState()
        servo_state.id = 1
        servo_state.position = int(pwm)  # Add .value to get integer
        servo_msg.state = [servo_state]
        servo_msg.duration = 0.1
        self.servo_pub.publish(servo_msg)
        
        # Check X button (index 2) for map saving
        x_button = msg.buttons[2]
        if x_button and not self.x_button_pressed:
            self.save_map()
        self.x_button_pressed = x_button
        
    def save_map(self):
        try:
            # Generate timestamp for filename
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            map_path = f'/home/robot/Documents/maps/map_{timestamp}'
            
            self.get_logger().info(f'Requesting map serialization to {map_path}...')
            
            # Create request
            request = SerializePoseGraph.Request()
            request.filename = map_path
            
            # Send request
            future = self.serialize_map_client.call_async(request)
            
            # Wait for response
            rclpy.spin_until_future_complete(self, future)
            
            if future.result() is not None:
                self.get_logger().info(f'Map successfully serialized to {map_path}')
            else:
                self.get_logger().error('Service call failed')
                
        except Exception as e:
            self.get_logger().error(f'Error saving map: {str(e)}')
            import traceback
            self.get_logger().error(f'Traceback: {traceback.format_exc()}')

def main(args=None):
    rclpy.init(args=args)
    node = XboxControlStation()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

