import os
from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
from launch.actions import SetEnvironmentVariable

def generate_launch_description():
    slam_params_file = "config/mapper_params_online_async.yaml"
    ekf_params_file = "config/ekf.yaml"
    SetEnvironmentVariable('ROS_LOG_DIR', '/home/yc/Documents/ROS2/ros_robot_controller-ros2/log_custom'),
    
    return LaunchDescription([
        # Start robot node
        Node(
            package='ros_robot_controller',
            executable='ros_robot_controller',
            name='robot_node',
            output='log',
        ),

        # Start lidar node
        Node(
            package='rplidar_ros',
            executable='rplidar_Node',
            name='rplidar',
            output='log',
        ),
        # Start IMU Odom Node
        Node(
            package='ros_robot_controller',
            executable='ackermann_odom_node',
            name='imu_odom',
            output='log',
        ),

        #Start EKF Node
        Node(
            package='robot_localization',
            executable='ekf_node',
            name='ekf_filter',
            output='log',
            parameters=[ekf_params_file]
        ),

        # Start slam node
        Node(
            package='slam_toolbox',
            executable='async_slam_toolbox_node',
            name='slam_toolbox',
            output='log',
            parameters=[slam_params_file]
        ),
    ])