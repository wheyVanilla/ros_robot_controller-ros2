import rclpy
from rclpy.node import Node
from tf2_ros import TransformBroadcaster
from geometry_msgs.msg import TransformStamped
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Quaternion


class DynamicTFBroadcaster(Node):
    def __init__(self):
        super().__init__('dynamic_tf_broadcaster')
        self.tf_broadcaster = TransformBroadcaster(self)
        self.timer = self.create_timer(0.1, self.broadcast_tf)  # Publish at 10Hz
        self.publisher_ = self.create_publisher(Odometry, '/odom', 10)
        self.timer = self.create_timer(0.1, self.publish_odom)  # Publish at 10 Hz
        self.x, self.y, self.theta = 0.0, 0.0, 0.0  # Initial position


    def broadcast_tf(self):
        t = TransformStamped()
        t.header.stamp = self.get_clock().now().to_msg()
        t.header.frame_id = "base_link"
        t.child_frame_id = "laser"
        t.transform.translation.x = 0.0  # Modify based on LIDAR position
        t.transform.translation.y = 0.0
        t.transform.translation.z = 0.1  # Example: LIDAR is 10cm above base_link
        t.transform.rotation.w = 1.0  # No rotation
        self.tf_broadcaster.sendTransform(t)
    def publish_odom(self):
        msg = Odometry()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = "odom"
        msg.child_frame_id = "base_link"

        # Simulate motion (modify this as needed)
        self.x += 0.1  # Move forward
        self.y += 0.0   # Stay on Y=0
        self.theta += 0.1  # Small rotation

        msg.pose.pose.position.x = self.x
        msg.pose.pose.position.y = self.y
        msg.pose.pose.position.z = 0.0

        # Convert yaw to quaternion
        msg.pose.pose.orientation = Quaternion(x=0.0, y=0.0, z=self.theta, w=1.0)

        # Simulate velocity
        msg.twist.twist.linear.x = 0.1  # Constant forward speed
        msg.twist.twist.angular.z = 0.00  # Small rotation

        self.publisher_.publish(msg)
        # self.get_logger().info(f"Published Odom: x={self.x}, y={self.y}, theta={self.theta}")

def main():
    rclpy.init()
    node = DynamicTFBroadcaster()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
