#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Imu
import yaml
import os

class MPU6050Calibration(Node):
    def __init__(self):
        super().__init__('mpu6050_calibration')
        self.subscription = self.create_subscription(Imu, 'robot_control/imu_raw', self.imu_callback, 1)
        
        self.samples = 500
        self.collection = 0
        self.accel_x_sum = 0
        self.accel_y_sum = 0
        self.accel_z_sum = 0
        self.gyro_x_sum = 0
        self.gyro_y_sum = 0
        self.gyro_z_sum = 0

        self.config_file = os.path.join(os.path.dirname(__file__), 'config', 'config.yaml')

        self.save_in_degrees = False

        self.get_logger().info('Calibrating MPU6050, Keeo the IMU stationary...')

    def imu_callback(self, msg):
        if self.collection < self.samples:
            self.accel_x_sum += msg.linear_acceleration.x
            self.accel_y_sum += msg.linear_acceleration.y
            self.accel_z_sum += msg.linear_acceleration.z
            self.gyro_x_sum += msg.angular_velocity.x
            self.gyro_y_sum += msg.angular_velocity.y
            self.gyro_z_sum += msg.angular_velocity.z
            self.collection += 1
            if self.collected % 100 == 0:
                self.get_logger().info(f"Collected {self.collected}/{self.samples} samples")
        else:
            # Calculate biases
            accel_x_bias = self.accel_x_sum / self.samples
            accel_y_bias = self.accel_y_sum / self.samples
            accel_z_bias = (self.accel_z_sum / self.samples) - 9.81  # Subtract 1g
            gyro_x_bias = self.gyro_x_sum / self.samples
            gyro_y_bias = self.gyro_y_sum / self.samples
            gyro_z_bias = self.gyro_z_sum / self.samples

            if self.save_in_degrees:
                gyro_unit = "degrees/s"
                gyro_x_bias_out = gyro_x_bias * 180 / 3.14159
                gyro_y_bias_out = gyro_y_bias * 180 / 3.14159
                gyro_z_bias_out = gyro_z_bias * 180 / 3.14159
            else:
                gyro_unit = "rad/s"
                gyro_x_bias_out = gyro_x_bias
                gyro_y_bias_out = gyro_y_bias
                gyro_z_bias_out = gyro_z_bias

            self.get_logger().info('Calibration complete!')
            self.get_logger().info(f"Accel X Bias: {accel_x_bias:.4f} m/s²")
            self.get_logger().info(f"Accel Y Bias: {accel_y_bias:.4f} m/s²")
            self.get_logger().info(f"Accel Z Bias: {accel_z_bias:.4f} m/s² (after removing 1g)")
            self.get_logger().info(f"Gyro X Bias: {gyro_x_bias_out:.4f} {gyro_unit}")
            self.get_logger().info(f"Gyro Y Bias: {gyro_y_bias_out:.4f} {gyro_unit}")
            self.get_logger().info(f"Gyro Z Bias: {gyro_z_bias_out:.4f} {gyro_unit}")
            self.get_logger().info("Calibration complete. Apply these biases to your IMU data.")

            self.save_to_config(
                accel_x_bias, accel_y_bias, accel_z_bias,
                gyro_x_bias_out, gyro_y_bias_out, gyro_z_bias_out,
                gyro_unit
            )

            self.get_logger().info(f'Calibration data saved to {self.config_file}')
            
            rclpy.shutdown()
    def save_to_config(self, accel_x_bias, accel_y_bias, accel_z_bias, gyro_x_bias, gyro_y_bias, gyro_z_bias, gyro_unit):
        
        try:
            with open(self.config_file, 'r') as file:
                config = yaml.safe_load(file) or {}
        except FileNotFoundError:
            config = {}
        
        config['ros_robot_controller'] = {
            'accelerometer': {
                'bias': {
                    'x': round(accel_x_bias, 4),
                    'y': round(accel_y_bias, 4),
                    'z': round(accel_z_bias, 4)
                },
                'scale': {
                    'x': 1.0,
                    'y': 1.0,
                    'z': 1.0
                }
            },
            'gyroscope': {
                'bias': {
                    'x': round(gyro_x_bias, 4),
                    'y': round(gyro_y_bias, 4),
                    'z': round(gyro_z_bias, 4)
                },
                'scale': {
                    'x': 1.0,
                    'y': 1.0,
                    'z': 1.0
                },
                'unit': gyro_unit
            }
        }

        with open(self.config_file, 'w') as file:
            yaml.dump(config, file, default_flow_style=False)

def main(args=None):
    rclpy.init(args=args)
    mpu6050_calibration = MPU6050Calibration()
    rclpy.spin(mpu6050_calibration)

if __name__ == '__main__':
    main()