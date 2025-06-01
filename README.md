# ROS2 Robot Controller

A ROS2-based robot control system featuring differential drive, servo steering, and SLAM capabilities. The system consists of two main packages:
- `ros_robot_controller`: Hardware interface and robot control (runs on Raspberry Pi)
- `ros_control_station`: Remote control interface (runs on laptop)

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

# Source workspace0
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

## Package Structure

### ros_robot_controller (Robot Side)
- Hardware interface with STM32
- IMU data processing
- Odometry calculation
- SLAM integration

### ros_control_station (Control Station)
- Xbox controller interface
- Remote control commands
- Vehicle selection

## Configuration

### Vehicle Parameters
Edit `src/ros_robot_controller/config/config.yaml`:
```yaml
vehicle_data:
  wheel_radius: 0.035    # meters
  wheelbase: 0.17        # meters
  servo_pwm_center: 1500 # microseconds
  servo_pwm_range: 2000  # microseconds
```

### IMU Calibration
Run calibration:
```bash
ros2 run ros_robot_controller mpu6050_calibration
```

## Control Mapping

Xbox Controller:
- Left Stick Up/Down: Forward/Backward
- Left Stick Left/Right: Steering
- X Button: Save SLAM Map
- Speed Range: ±1.5 RPS
- Steering Range: ±45°

### Map Saving
Press X button on the Xbox controller to save the current SLAM map. Maps are saved in `~/maps` directory with timestamp-based filenames.

### Additional Dependencies
```bash
# Install nav2_map_server for map saving
sudo apt install ros-jazzy-nav2-map-server
```

## Development

Build packages:
```bash
# Build specific package
colcon build --packages-select ros_robot_controller

# Build all packages
colcon build
```

## Troubleshooting

1. **USB Port Access**:
```bash
sudo usermod -a -G dialout $USER
sudo chmod 666 /dev/ttyACM0  # For STM32
sudo chmod 666 /dev/ttyUSB0  # For RPLidar
```

2. **Xbox Controller**:
```bash
# Check controller
ls /dev/input/js0
```

## License
[Your License]

## Author
[Your Name]
```

