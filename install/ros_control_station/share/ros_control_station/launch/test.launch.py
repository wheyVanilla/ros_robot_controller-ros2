from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import SetEnvironmentVariable

def generate_launch_description():
    return LaunchDescription([

        SetEnvironmentVariable('ROS_LOG_DIR', '/home/yc/Documents/ROS2/ros_robot_controller-ros2/logg'),
        # Joy node
        Node(
            package='joy',
            executable='joy_node',
            name='joy_node',
            parameters=[{
                'dev': '/dev/input/js0',  # Xbox controller device
                'deadzone': 0.05,         # Ignore small movements
                'autorepeat_rate': 20.0,  # Hz
            }]
        ),
        
                # LED node
        Node(
            package='ros_control_station',
            executable='vehicle_control_station',
            name='vehicle_control_station',
            output='log'
        )
    ])
