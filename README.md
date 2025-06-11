# ROS2 Robot Controller

A ROS2-based robot control system featuring ackerman drive, servo steering, and SLAM capabilities. The system consists of two main packages:
- `ros_robot_controller`: Hardware interface and robot control (runs on Raspberry Pi), interfacing STM32 controller
- `ros_control_station`: Remote control interface (runs on laptop)

![IMG_9015](https://github.com/user-attachments/assets/3781c054-fcaa-4ea5-bb04-8450feb3daa4)


## System Requirements

### Hardware
- Raspberry Pi 5
- STM32 Controller Board
- MPU6050 IMU
- RPLidar A1
- Xbox Controller
- PWM Servo
- DC Motors with Encoders

### Software
- ROS2 Jazzy
- Python 3.12
- robot_localization
- slam_toolbox
- rplidar_ros
- joy

## Quick Start

1. **Setup ROS2 Environment**:
```bash
# Source ROS2
source /opt/ros/jazzy/setup.bash

# Source workspace
source install/setup.bash
```

2. **On Control Station (Laptop)**:
```bash
# Launch Xbox controller interface
ros2 launch ros_control_station ros_control_station.launch.py
```

3. **On Robot (Raspberry Pi)**:
```bash
# Launch robot controller and SLAM
ros2 launch ros_robot_controller slam_localization.launch.py
```

## Deployment (Automated)

For easy deployment, you can use the provided script to package, transfer, and build the source code on the target robots.

### Prerequisites
The script requires the robot's sudo password to set up services. Set it as an environment variable on your control station before running the script:
```bash
export SUDO_PASS='your_robot_sudo_password'
```

### How to Run
To deploy to one or more robots, run the following command from your workspace root, replacing `<robot_ip>` with your robot's actual IP address:
```bash
./src/ros_control_station/scripts/deploy/deploy_to_robots.sh <robot_ip_1> [robot_ip_2] ...
```
The script will handle building the code and setting up the systemd service to run the robot's software on startup.

## Package Structure

### ros_robot_controller (Robot Side)
Main hardware interface package with the following nodes:
- **ros_robot_controller**: Hardware interface with STM32, IMU data processing
- **odom_node**: Ackermann odometry calculation from motor encoders and IMU
- **tf_publisher**: Static transform publisher for robot frames
- **mpu6050_calibration**: IMU calibration utility

Key features:
- Hardware interface with STM32 controller board
- IMU data processing and bias correction
- Odometry calculation using motor encoders and IMU fusion
- Support for manual control mode with vehicle selection
- Servo and motor control through custom messages

### ros_control_station (Control Station)
Remote control interface with the following nodes:
- **xbox_controller**: Xbox controller interface for robot control
- **vehicle_control_station**: GUI-based vehicle selection interface

Key features:
- Xbox controller mapping for robot movement and steering
- Map saving functionality (X button saves SLAM maps)
- Vehicle selection GUI using tkinter
- Real-time control with configurable speed and steering limits

## Configuration

The system uses YAML configuration files for robot and control station settings. For detailed configuration options, see [CONFIGURATION.md](CONFIGURATION.md).

### Quick Configuration
- **Robot parameters**: Edit `src/ros_robot_controller/config/config.yaml`
- **Control station**: Edit `src/ros_control_station/config/config.yaml`
- **IMU calibration**: Run `ros2 run ros_robot_controller mpu6050_calibration`

## Control Mapping

### Xbox Controller
- **Left Stick Up/Down**: Forward/Backward movement
- **Left Stick Left/Right**: Steering control
- **Right Stick Up/Down**: Navigate vehicle selection menu
- **A Button**: Select vehicle from menu
- **X Button**: Save SLAM map to `/home/robot/Documents/maps/`
- **Speed Range**: ±1.5 RPS (configurable)
- **Steering Range**: ±36° (configurable)

### Vehicle Selection
The system supports multiple robots through a vehicle selection interface:
1. Use the right joystick to navigate through available vehicles
2. Press A button to select a vehicle
3. Selected vehicle's LED will light up for confirmation
4. Vehicle identification is based on CPU serial number

### Map Saving
Press X button on the Xbox controller to save the current SLAM map. Maps are automatically saved with timestamp-based filenames:
- Location: `/home/robot/Documents/maps/`
- Format: `map_YYYYMMDD_HHMMSS`
- Includes both `.pgm` and `.yaml` files

### Launch Files
#### Control Station
```bash
# Launch complete control station (joy + xbox_controller + vehicle_selection)
ros2 launch ros_control_station ros_control_station.launch.py
```

#### Robot
```bash
# Launch robot with SLAM and localization
ros2 launch ros_robot_controller slam_localization.launch.py
```

The robot launch file includes:
- STM32 hardware interface
- IMU processing and odometry calculation
- EKF sensor fusion
- RPLidar integration
- SLAM Toolbox for mapping

### Service Configuration
The robot can be configured to start automatically on boot using systemd:
- Service file: `src/ros_robot_controller/scripts/robot_launcher.service`
- Startup script: `src/ros_robot_controller/scripts/start_robot.sh`

## Development

### Building the Workspace
```bash
# Build specific package
colcon build --packages-select ros_robot_controller
colcon build --packages-select ros_control_station

# Build all packages
colcon build

# Build with debug symbols
colcon build --cmake-args -DCMAKE_BUILD_TYPE=Debug
```

### Available Executables
#### ros_robot_controller package:
- `ros_robot_controller`: Main hardware interface node
- `odom_node`: Odometry calculation node
- `tf_publisher`: Transform publisher node
- `mpu6050_calibration`: IMU calibration utility

#### ros_control_station package:
- `xbox_controller`: Xbox controller interface node
- `vehicle_control_station`: Vehicle selection GUI node

### Dependencies
The packages depend on:
- `rclpy`: Python ROS2 client library
- `sensor_msgs`: Standard sensor message definitions
- `nav_msgs`: Navigation message definitions (for odometry)
- `geometry_msgs`: Geometry message definitions
- `std_msgs`: Standard message definitions
- `tf2_ros`: Transform library
- `robot_localization`: EKF sensor fusion
- `slam_toolbox`: SLAM implementation
- `rplidar_ros`: RPLidar driver
- `joy`: Joystick/gamepad interface

## Troubleshooting

### USB Port Access
```bash
# Add user to dialout group for serial port access
sudo usermod -a -G dialout $USER

# Set permissions for hardware devices
sudo chmod 666 /dev/ttyACM0  # For STM32 controller board
sudo chmod 666 /dev/ttyUSB0  # For RPLidar

# Create persistent udev rules (optional)
sudo cp src/ros_robot_controller/scripts/99-ttyACM0.rules /etc/udev/rules.d/
sudo udevadm control --reload-rules
```

### Xbox Controller Issues
```bash
# Check if controller is detected
ls /dev/input/js0

# Test controller input
jstest /dev/input/js0

# Install joy package if missing
sudo apt install ros-jazzy-joy
```

### IMU Calibration Issues
```bash
# If IMU readings are incorrect, recalibrate
ros2 run ros_robot_controller mpu6050_calibration

# Check IMU data
ros2 topic echo /robot_control/imu_raw
ros2 topic echo /robot_control/imu
```

### SLAM Issues
```bash
# Check if RPLidar is working
ros2 topic echo /scan

# Verify odometry
ros2 topic echo /odom

# Check EKF output
ros2 topic echo /odometry/filtered
```

### Network Issues
```bash
# Check ROS_DOMAIN_ID
echo $ROS_DOMAIN_ID

# Test communication between control station and robot
ros2 topic list
ros2 node list
```

## License
[Your License]

## Author
[Your Name]
```

