#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
from geometry_msgs.msg import TransformStamped, Quaternion
from tf2_ros import TransformBroadcaster
import math
from ros_robot_controller_msgs.msg import MotorsState, PWMServoState
import ros_robot_controller.utils as utils
from sensor_msgs.msg import Imu

class OdomCalcNode(Node):
    def __init__(self):
        super().__init__('odom_calc_node')

        # Declare config path parameter and load config
        self.declare_parameter('config_path', 'src/ros_robot_controller/config/config.yaml')
        config_path = self.get_parameter('config_path').get_parameter_value().string_value
        self.config = utils.load_config(self, config_key='vehicle_data', config_path=config_path)

        # Vehicle parameters from config
        self.wheel_radius = self.config.get('wheel_radius', 0.035)
        self.wheelbase = self.config.get('wheelbase', 0.17)
        self.servo_pwm_center = self.config.get('servo_pwm_center', 1500)
        self.servo_pwm_range = self.config.get('servo_pwm_range', 1000)
        steering_max_normalized = self.config.get('steering_angle_max', 1.0)
        self.steering_angle_max = steering_max_normalized * (math.pi)

        # Covariance from config
        self.pose_covariance = self.config.get('pose_covariance', [
            0.0004, 0.0, 0.0, 0.0, 0.0, 0.0,  # x (±0.02 m)
            0.0, 0.0004, 0.0, 0.0, 0.0, 0.0,  # y (±0.02 m)
            0.0, 0.0, 1000.0, 0.0, 0.0, 0.0,  # z
            0.0, 0.0, 0.0, 1000.0, 0.0, 0.0,  # roll
            0.0, 0.0, 0.0, 0.0, 1000.0, 0.0,  # pitch
            0.0, 0.0, 0.0, 0.0, 0.0, 0.0012   # yaw (±2°)
        ])
        self.twist_covariance = self.config.get('twist_covariance', [
            0.0005, 0.0, 0.0, 0.0, 0.0, 0.0,  # vx (±0.022 m/s)
            0.0, 1000.0, 0.0, 0.0, 0.0, 0.0,  # vy
            0.0, 0.0, 1000.0, 0.0, 0.0, 0.0,  # vz
            0.0, 0.0, 0.0, 1000.0, 0.0, 0.0,  # wx
            0.0, 0.0, 0.0, 0.0, 1000.0, 0.0,  # wy
            0.0, 0.0, 0.0, 0.0, 0.0, 0.0076  # wz (±0.087 rad/s)
        ])

        # Robot state
        self.x = 0.0
        self.y = 0.0
        self.theta = 0.0
        self.v_linear = 0.0
        self.v_angular = 0.0
        self.steering_angle = 0.0
        self.last_time = self.get_clock().now()

        # Subscribers
        self.motor_sub = self.create_subscription(MotorsState, 'robot_control/motors', self.motor_callback, 10)
        self.imu_sub = self.create_subscription(
            Imu,
            'robot_control/imu',  # Using corrected IMU data
            self.imu_callback,
            10
        )

        # Publisher and TF broadcaster
        self.odom_pub = self.create_publisher(Odometry, '/odom', 10)
        self.tf_broadcaster = TransformBroadcaster(self)

        self.get_logger().info('Odometry calculation node started')
        self.get_logger().info(
            f"Vehicle parameters: wheel_radius={self.wheel_radius}m, "
            f"wheelbase={self.wheelbase}m, "
            f"servo_pwm_center={self.servo_pwm_center}us, "
            f"servo_pwm_range={self.servo_pwm_range}us, "
            f"steering_angle_max={math.degrees(self.steering_angle_max):.1f}° "
            f"(normalized: {steering_max_normalized})"
        )

    def imu_callback(self, msg):
        # Use IMU orientation directly if available
        if msg.orientation.w != 1.0:  # Check if real orientation data exists
            self.theta = utils.yaw_from_quaternion(msg.orientation)
        # Use angular velocity as backup/complement
        self.v_angular = msg.angular_velocity.z
        
        # No need to calculate v_angular from steering angle anymore
        # self.v_angular = -self.v_linear * math.tan(self.steering_angle) / self.wheelbase

    def motor_callback(self, msg):
        current_time = self.get_clock().now()
        dt = (current_time - self.last_time).nanoseconds * 1e-9

        motor_speeds = {m.id: m.rps for m in msg.data}
        left_rps = motor_speeds.get(0, 0.0)
        right_rps = motor_speeds.get(1, 0.0)

        left_speed = left_rps * 2 * math.pi * self.wheel_radius
        right_speed = -right_rps * 2 * math.pi * self.wheel_radius
        self.v_linear = (left_speed + right_speed) / 2.0

        if dt > 0:
            self.x += self.v_linear * math.cos(self.theta) * dt
            self.y += self.v_linear * math.sin(self.theta) * dt
            self.theta += self.v_angular * dt
            self.theta = utils.normalize_angle(self.theta)
            self._publish_odom(current_time)

        self.last_time = current_time

    def servo_callback(self, msg):
        pass

    def _publish_odom(self, current_time):
        odom = Odometry()
        odom.header.stamp = current_time.to_msg()
        odom.header.frame_id = 'odom'
        odom.child_frame_id = 'base_link'

        odom.pose.pose.position.x = self.x
        odom.pose.pose.position.y = self.y
        odom.pose.pose.position.z = 0.0
        odom.pose.pose.orientation = utils.quaternion_from_yaw(self.theta)

        odom.twist.twist.linear.x = self.v_linear
        odom.twist.twist.linear.y = 0.0
        odom.twist.twist.angular.z = self.v_angular

        odom.pose.covariance = self.pose_covariance
        odom.twist.covariance = self.twist_covariance

        self.odom_pub.publish(odom)

        t = TransformStamped()
        t.header.stamp = current_time.to_msg()
        t.header.frame_id = 'odom'
        t.child_frame_id = 'base_link'
        t.transform.translation.x = self.x
        t.transform.translation.y = self.y
        t.transform.translation.z = 0.0
        t.transform.rotation = utils.quaternion_from_yaw(self.theta)
        self.tf_broadcaster.sendTransform(t)

def main(args=None):
    rclpy.init(args=args)
    node = OdomCalcNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()