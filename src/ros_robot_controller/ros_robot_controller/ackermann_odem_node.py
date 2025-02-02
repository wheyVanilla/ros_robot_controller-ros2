import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
from sensor_msgs.msg import Imu
from geometry_msgs.msg import Quaternion, TransformStamped
from tf2_ros import TransformBroadcaster
import math

class IMUOdemNode(Node):
    def __init__(self):
        super().__init__('imu_odom_node')
        self.odom_pub = self.create_publisher(Odometry, '/odom/filtered', 10)
        self.tf_broadcaster = TransformBroadcaster(self)

        self.imu_sub = self.create_subscription(Imu, '/robot_control/imu_raw', self.imu_callback, 10)
        
        self.wheelbase = 180 # mm
        
        self.x = 0.0    # x position
        self.y = 0.0    # y position
        self.yaw = 0.0  # yaw angle
        self.vx =  0.0  # longitudinal velocity
        self.vy = 0.0   # lateral velocity
        self.last_time = self.get_clock().now()

    def imu_callback(self, msg):
        current_time = self.get_clock().now()
        dt = (current_time - self.last_time).nanoseconds * 1e-9

        angular_velocity = msg.angular_velocity.z # rad/s
        self.yaw += angular_velocity*dt # rad

        self.ax = msg.linear_acceleration.x     # m/s^2
        self.ay = msg.linear_acceleration.y     # m/s^2

        self.vx += self.ax * dt   # m/s
        self.vy += self.ay * dt   # m/s

        self.x += self.vx * dt  # m
        self.y += self.vx * dt  # m

        # Publish odometry message
        odom = Odometry()
        odom.header.stamp = current_time.to_msg()
        odom.header.frame_id = 'odom'
        odom.child_frame_id = 'base_link'

        odom.pose.pose.position.x = self.x
        odom.pose.pose.position.y = self.y
        odom.pose.pose.position.z = 0.0
        odom.pose.pose.orientation = Quaternion(x=0.0, y=0.0, z=math.sin(self.yaw/2), w=math.cos(self.yaw/2))

        odom.twist.twist.linear.x = self.vx
        odom.twist.twist.linear.y = self.vy
        odom.twist.twist.angular.z = angular_velocity

        self.odom_pub.publish(odom)

        # Publish tf
        t = TransformStamped()
        t.header.stamp = current_time.to_msg()
        t.header.frame_id = 'odom'
        t.child_frame_id = 'base_link'
        t.transform.translation.x = self.x
        t.transform.translation.y = self.y
        t.transform.translation.z = 0.0
        t.transform.rotation.z = math.sin(self.yaw/2)
        t.transform.rotation.w = math.cos(self.yaw/2)

        self.tf_broadcaster.sendTransform(t)

        self.last_time = current_time


    def drive_callback(self, msg):
        steering_angle = msg.drive.steering_angle
        self.v = msg.drive.speed

def main(args=None):
    rclpy.init(args=args)
    imu_odom_node = IMUOdemNode()
    rclpy.spin(imu_odom_node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
