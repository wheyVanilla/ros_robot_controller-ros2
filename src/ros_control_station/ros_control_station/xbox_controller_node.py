#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Joy
from ros_robot_controller_msgs.msg import MotorsState, MotorState, PWMServoState, SetPWMServoState
from rclpy.qos import QoSProfile, ReliabilityPolicy
from ctypes import c_uint16 as uint16

class XboxControlStation(Node):
    def __init__(self):
        super().__init__('xbox_control_station')
        
        # Create QoS profile for controller
        qos = QoSProfile(
            depth=1,
            reliability=ReliabilityPolicy.BEST_EFFORT
        )

        # Control parameters
        self.max_speed = 2.0     # Maximum RPS
        
        # Servo parameters
        self.center_pwm = 1500   # Center position (90°)
        self.pwm_range = 1000    # PWM range from center (±1000)
        self.max_turn = 1      # Maximum turn range (0.5 = ±45°)
        
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
        
    def map_to_pwm(self, turn_value):
        """Map joystick (-1 to 1) to PWM range (500-2500)"""
        # Limit turn range
        turn_value = max(min(turn_value, self.max_turn), -self.max_turn)
        # Map to PWM and ensure it's an integer
        pwm = int(self.center_pwm - (turn_value * self.pwm_range / self.max_turn))
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
        
def main(args=None):
    rclpy.init(args=args)
    node = XboxControlStation()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

