import os
from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
from launch.actions import SetEnvironmentVariable

def generate_launch_description():
    SetEnvironmentVariable('ROS_LOG_DIR', 'log_custom'),
    slam_params_file = "/home/robot/Documents/ros2/config/mapper_params_online_async.yaml"
    ekf_params_file = "src/ros_robot_controller/config/ekf.yaml"
    
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
            executable='rplidar_composition',
            name='rplidar',
            output='screen',
            parameters=[{
                'serial_port': '/dev/ttyUSB0',
                'serial_baudrate': 115200,
                'frame_id': 'laser',
                'inverted': False,
                'angle_compensate': True
            }]
        ),
        # Start IMU Odom Node
        # Node(
        #     package='ros_robot_controller',
        #     executable='imu_odom_node',
        #     name='imu_odom',
        #     output='screen',
        # ),

        Node(
            package='ros_robot_controller',
            executable='tf_publisher',
            name='temp_tf_publisher',
            output='screen',
        ),

        #Start EKF Node
        Node(
            package='robot_localization',
            executable='ekf_node',
            name='ekf_filter',
            output='screen',
            parameters=[ekf_params_file]
        ),

        # Start slam node
        # Node(
        #     package='slam_toolbox',
        #     executable='async_slam_toolbox_node',
        #     name='slam_toolbox',
        #     output='screen',
        #     parameters=[{'slam_params_file':slam_params_file}]
        # )
    ])