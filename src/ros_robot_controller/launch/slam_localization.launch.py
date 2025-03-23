import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, EmitEvent, LogInfo, RegisterEventHandler, SetEnvironmentVariable
from launch.conditions import IfCondition
from launch.events import matches_action
from launch.substitutions import LaunchConfiguration, AndSubstitution, NotSubstitution
from launch_ros.actions import Node, LifecycleNode
from launch_ros.event_handlers import OnStateTransition
from launch_ros.events.lifecycle import ChangeState
from lifecycle_msgs.msg import Transition
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    # Launch configurations
    autostart = LaunchConfiguration('autostart')
    use_lifecycle_manager = LaunchConfiguration('use_lifecycle_manager')
    use_sim_time = LaunchConfiguration('use_sim_time')
    
    # Static file paths
    slam_params_file = "src/ros_robot_controller/config/mapper_params_online_async.yaml"
    ekf_params_file = "src/ros_robot_controller/config/ekf.yaml"

    # Launch arguments
    declare_autostart = DeclareLaunchArgument(
        'autostart', 
        default_value='true',
        description='Automatically startup the slamtoolbox'
    )
    
    declare_use_lifecycle_manager = DeclareLaunchArgument(
        'use_lifecycle_manager',
        default_value='false',
        description='Enable bond connection during node activation'
    )
    
    declare_use_sim_time = DeclareLaunchArgument(
        'use_sim_time',
        default_value='true',
        description='Use simulation/Gazebo clock'
    )

    # SLAM Toolbox Lifecycle Node
    start_async_slam_toolbox_node = LifecycleNode(
        package='slam_toolbox',
        executable='async_slam_toolbox_node',
        name='slam_toolbox',
        output='screen',
        namespace='',
        parameters=[
            slam_params_file,
            {
                'use_lifecycle_manager': use_lifecycle_manager,
                'use_sim_time': use_sim_time
            }
        ]
    )

    # Lifecycle events for automatic configuration and activation
    configure_event = EmitEvent(
        event=ChangeState(
            lifecycle_node_matcher=matches_action(start_async_slam_toolbox_node),
            transition_id=Transition.TRANSITION_CONFIGURE
        ),
        condition=IfCondition(AndSubstitution(autostart, NotSubstitution(use_lifecycle_manager)))
    )

    activate_event = RegisterEventHandler(
        OnStateTransition(
            target_lifecycle_node=start_async_slam_toolbox_node,
            start_state="configuring",
            goal_state="inactive",
            entities=[
                LogInfo(msg="[LifecycleLaunch] Slamtoolbox node is activating."),
                EmitEvent(event=ChangeState(
                    lifecycle_node_matcher=matches_action(start_async_slam_toolbox_node),
                    transition_id=Transition.TRANSITION_ACTIVATE
                ))
            ]
        ),
        condition=IfCondition(AndSubstitution(autostart, NotSubstitution(use_lifecycle_manager)))
    )

    # Create LaunchDescription
    ld = LaunchDescription([
        # Environment variable
        SetEnvironmentVariable('ROS_LOG_DIR', 'log_custom'),
        
        # Launch arguments
        declare_autostart,
        declare_use_lifecycle_manager,
        declare_use_sim_time,

        # Robot controller node
        Node(
            package='ros_robot_controller',
            executable='ros_robot_controller',
            name='robot_node',
            output='log'
        ),

        # RPLidar node
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

        # IMU Odometry node
        Node(
            package='ros_robot_controller',
            executable='imu_odom_node',
            name='imu_odom',
            output='screen'
        ),

        # TF Publisher node
        Node(
            package='ros_robot_controller',
            executable='tf_publisher',
            name='temp_tf_publisher',
            output='screen'
        ),

        # EKF Node
        Node(
            package='robot_localization',
            executable='ekf_node',
            name='ekf_filter',
            output='screen',
            parameters=[ekf_params_file]
        ),

        # SLAM Toolbox node with lifecycle events
        start_async_slam_toolbox_node,
        configure_event,
        activate_event
    ])

    return ld