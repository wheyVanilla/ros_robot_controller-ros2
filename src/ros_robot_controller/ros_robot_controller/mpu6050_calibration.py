#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Imu
import yaml
import os
import logging
from datetime import datetime

class ImuCalibrationNode(Node):
    def __init__(self):
        super().__init__('mpu6050_calibration')

        # Set up standalone Python logger for file output
        log_dir = os.path.expanduser('~/log_costom')
        os.makedirs(log_dir, exist_ok=True)
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        log_file = os.path.join(log_dir, f'calibration_{timestamp}.log')

        # Configure custom logger
        self.file_logger = logging.getLogger('mpu6050_calibration_file')
        self.file_logger.setLevel(logging.INFO)
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s [%(levelname)s] [%(name)s]: %(message)s')
        file_handler.setFormatter(formatter)
        self.file_logger.addHandler(file_handler)

        # Log initial message to both console (ROS logger) and file
        self.get_logger().info(f"Logging initialized to {log_file}")
        self.file_logger.info(f"Logging initialized to {log_file}")

        self.subscription = self.create_subscription(
            Imu,
            'robot_control/imu_raw',
            self.imu_callback,
            1
        )
        self.samples = 500
        self.runs = 4
        self.current_run = 0
        self.collected = 0
        self.waiting_for_input = False
        self.accel_sums = {'x': 0.0, 'y': 0.0, 'z': 0.0}
        self.gyro_sums = {'x': 0.0, 'y': 0.0, 'z': 0.0}
        self.accel_bias_array = {'x': 0.0, 'y': 0.0, 'z': 0.0}
        self.gyro_bias_array = {'x': 0.0, 'y': 0.0, 'z': 0.0}

        self.declare_parameter('config_path', 'src/ros_robot_controller/config/config.yaml')
        self.config_path = self.get_parameter('config_path').get_parameter_value().string_value

        self.save_in_degrees = True
        self.get_logger().info(f"Run {self.current_run + 1}/{self.runs}: Keep IMU stationary...")
        self.file_logger.info(f"Run {self.current_run + 1}/{self.runs}: Keep IMU stationary...")

    def imu_callback(self, msg):
        if self.waiting_for_input:
            return

        if self.collected < self.samples:
            self.accel_sums['x'] += msg.linear_acceleration.x
            self.accel_sums['y'] += msg.linear_acceleration.y
            self.accel_sums['z'] += msg.linear_acceleration.z
            self.gyro_sums['x'] += msg.angular_velocity.x
            self.gyro_sums['y'] += msg.angular_velocity.y
            self.gyro_sums['z'] += msg.angular_velocity.z

            self.collected += 1
            if self.collected % 100 == 0:
                log_msg = f"Run {self.current_run + 1}: Collected {self.collected}/{self.samples}"
                self.get_logger().info(log_msg)
                self.file_logger.info(log_msg)

        if self.collected >= self.samples:
            self.collected = 0

            accel_x_bias = self.accel_sums['x'] / self.samples
            accel_y_bias = self.accel_sums['y'] / self.samples
            accel_z_bias = (self.accel_sums['z'] / self.samples) - 9.81
            gyro_x_bias = self.gyro_sums['x'] / self.samples
            gyro_y_bias = self.gyro_sums['y'] / self.samples
            gyro_z_bias = self.gyro_sums['z'] / self.samples
            gyro_x_bias_out = gyro_x_bias * 180 / 3.14159
            gyro_y_bias_out = gyro_y_bias * 180 / 3.14159
            gyro_z_bias_out = gyro_z_bias * 180 / 3.14159
            gyro_unit = "degrees/s"

            self.accel_bias_array['x'] += accel_x_bias
            self.accel_bias_array['y'] += accel_y_bias
            self.accel_bias_array['z'] += accel_z_bias
            self.gyro_bias_array['x'] += gyro_x_bias
            self.gyro_bias_array['y'] += gyro_y_bias
            self.gyro_bias_array['z'] += gyro_z_bias

            self.get_logger().info(f'{self.current_run + 1} Calibration Completed!')
            self.file_logger.info(f'{self.current_run + 1} Calibration Completed!')
            self.get_logger().info(f"Accel X Bias: {accel_x_bias:.4f} m/s²")
            self.file_logger.info(f"Accel X Bias: {accel_x_bias:.4f} m/s²")
            self.get_logger().info(f"Accel Y Bias: {accel_y_bias:.4f} m/s²")
            self.file_logger.info(f"Accel Y Bias: {accel_y_bias:.4f} m/s²")
            self.get_logger().info(f"Accel Z Bias: {accel_z_bias:.4f} m/s² (after removing 1g)")
            self.file_logger.info(f"Accel Z Bias: {accel_z_bias:.4f} m/s² (after removing 1g)")
            self.get_logger().info(f"Gyro X Bias: {gyro_x_bias_out:.4f} {gyro_unit}")
            self.file_logger.info(f"Gyro X Bias: {gyro_x_bias_out:.4f} {gyro_unit}")
            self.get_logger().info(f"Gyro Y Bias: {gyro_y_bias_out:.4f} {gyro_unit}")
            self.file_logger.info(f"Gyro Y Bias: {gyro_y_bias_out:.4f} {gyro_unit}")
            self.get_logger().info(f"Gyro Z Bias: {gyro_z_bias_out:.4f} {gyro_unit}")
            self.file_logger.info(f"Gyro Z Bias: {gyro_z_bias_out:.4f} {gyro_unit}")

            self.current_run += 1
            self.accel_sums = {'x': 0.0, 'y': 0.0, 'z': 0.0}
            self.gyro_sums = {'x': 0.0, 'y': 0.0, 'z': 0.0}

            if self.current_run < self.runs:
                self.waiting_for_input = True
                self.get_logger().info(f"Move IMU to new position. Press Enter to start Run {self.current_run + 1}/{self.runs}...")
                self.file_logger.info(f"Move IMU to new position. Press Enter to start Run {self.current_run + 1}/{self.runs}...")
                try:
                    input()
                except KeyboardInterrupt:
                    self.get_logger().info("Calibration interrupted.")
                    self.file_logger.info("Calibration interrupted.")
                    rclpy.shutdown()
                    return
                self.waiting_for_input = False
                self.get_logger().info(f"Run {self.current_run + 1}/{self.runs}: Keep IMU stationary...")
                self.file_logger.info(f"Run {self.current_run + 1}/{self.runs}: Keep IMU stationary...")
            else:
                accel_x_bias = self.accel_bias_array['x'] / self.runs
                accel_y_bias = self.accel_bias_array['y'] / self.runs
                accel_z_bias = self.accel_bias_array['z'] / self.runs
                gyro_x_bias = self.gyro_bias_array['x'] / self.runs
                gyro_y_bias = self.gyro_bias_array['y'] / self.runs
                gyro_z_bias = self.gyro_bias_array['z'] / self.runs

                gyro_x_bias_out = gyro_x_bias * 180 / 3.14159
                gyro_y_bias_out = gyro_y_bias * 180 / 3.14159
                gyro_z_bias_out = gyro_z_bias * 180 / 3.14159
                gyro_unit = "degrees/s"

                self.get_logger().info("\nAveraged Calibration Results:")
                self.file_logger.info("\nAveraged Calibration Results:")
                self.get_logger().info(f"Accel X Bias: {accel_x_bias:.4f} m/s²")
                self.file_logger.info(f"Accel X Bias: {accel_x_bias:.4f} m/s²")
                self.get_logger().info(f"Accel Y Bias: {accel_y_bias:.4f} m/s²")
                self.file_logger.info(f"Accel Y Bias: {accel_y_bias:.4f} m/s²")
                self.get_logger().info(f"Accel Z Bias: {accel_z_bias:.4f} m/s² (after removing 1g)")
                self.file_logger.info(f"Accel Z Bias: {accel_z_bias:.4f} m/s² (after removing 1g)")
                self.get_logger().info(f"Gyro X Bias: {gyro_x_bias_out:.4f} {gyro_unit}")
                self.file_logger.info(f"Gyro X Bias: {gyro_x_bias_out:.4f} {gyro_unit}")
                self.get_logger().info(f"Gyro Y Bias: {gyro_y_bias_out:.4f} {gyro_unit}")
                self.file_logger.info(f"Gyro Y Bias: {gyro_y_bias_out:.4f} {gyro_unit}")
                self.get_logger().info(f"Gyro Z Bias: {gyro_z_bias_out:.4f} {gyro_unit}")
                self.file_logger.info(f"Gyro Z Bias: {gyro_z_bias_out:.4f} {gyro_unit}")

                self.save_to_config(accel_x_bias, accel_y_bias, accel_z_bias,
                                   gyro_x_bias_out, gyro_y_bias_out, gyro_z_bias_out, gyro_unit)
                self.get_logger().info(f"Calibration saved to {self.config_path}")
                self.file_logger.info(f"Calibration saved to {self.config_path}")

                # Flush file logger before shutdown
                for handler in self.file_logger.handlers:
                    handler.flush()
                rclpy.shutdown()

    def save_to_config(self, accel_x_bias, accel_y_bias, accel_z_bias,
                      gyro_x_bias, gyro_y_bias, gyro_z_bias, gyro_unit):
        try:
            with open(self.config_path, 'r') as f:
                config = yaml.safe_load(f) or {}
        except FileNotFoundError:
            config = {}

        if 'ros_robot_controller_node' not in config:
            config['ros_robot_controller_node'] = {'frequency': 10}

        config['ros_robot_controller_node']['imu_calibration'] = {
            'accelerometer': {
                'bias': {
                    'x': round(accel_x_bias, 4),
                    'y': round(accel_y_bias, 4),
                    'z': round(accel_z_bias, 4)
                },
                'scale': {'x': 1.0, 'y': 1.0, 'z': 1.0}
            },
            'gyroscope': {
                'bias': {
                    'x': round(gyro_x_bias, 4),
                    'y': round(gyro_y_bias, 4),
                    'z': round(gyro_z_bias, 4)
                },
                'scale': {'x': 1.0, 'y': 1.0, 'z': 1.0},
                'unit': gyro_unit
            }
        }

        with open(self.config_path, 'w') as f:
            yaml.dump(config, f, default_flow_style=False)

def main(args=None):
    rclpy.init(args=args)
    node = ImuCalibrationNode()
    rclpy.spin(node)

if __name__ == '__main__':
    main()