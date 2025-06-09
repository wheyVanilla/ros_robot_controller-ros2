# Configuration Guide

This document provides detailed configuration options for the ROS2 Robot Controller system.

## Robot Controller Configuration

### File Location
Edit `src/ros_robot_controller/config/config.yaml`

### Vehicle Parameters
```yaml
vehicle_data:
  wheel_radius: 0.035        # meters - Physical wheel radius
  wheelbase: 0.17           # meters - Distance between front and rear axles
  servo_pwm_center: 1500    # microseconds - Servo center position (90°)
  servo_pwm_range: 2000     # ±microseconds - PWM range from center
  steering_angle_max: 1.0   # 1 for ±90 degrees - Maximum steering angle
  correction_factor: 1.106   # Correction factor for calculated speed
```

### Node Frequencies
```yaml
ros_robot_controller_node:
  frequency:
    all: 10      # General publishing frequency (Hz)
    imu: 20      # IMU data frequency (Hz)
    encoder: 10  # Motor encoder frequency (Hz)
    servo: 10    # Servo control frequency (Hz)
```

### IMU Calibration
```yaml
imu_calibration:
  accelerometer:
    bias:
      x: 0.3273    # Accelerometer X-axis bias
      y: -0.3155   # Accelerometer Y-axis bias
      z: 0.1695    # Accelerometer Z-axis bias
    scale:
      x: 1.0       # Accelerometer X-axis scale
      y: 1.0       # Accelerometer Y-axis scale
      z: 1.0       # Accelerometer Z-axis scale
  gyroscope:
    bias:
      x: -1.3350   # Gyroscope X-axis bias
      y: -15.6098  # Gyroscope Y-axis bias
      z: 1.3329    # Gyroscope Z-axis bias
    scale:
      x: 1.0       # Gyroscope X-axis scale
      y: 1.0       # Gyroscope Y-axis scale
      z: 1.0       # Gyroscope Z-axis scale
    unit: degree/s # Gyroscope units
```

### IMU Covariance Parameters
```yaml
imu_parameters:
  orientation_covariance: [0.0012, 0, 0,    # roll (±2°)
                         0, 0.0012, 0,      # pitch (±2°)
                         0, 0, 0.0012]      # yaw (±2°)
  angular_velocity_covariance: [0.0076, 0, 0,  # roll rate
                              0, 0.0076, 0,    # pitch rate
                              0, 0, 0.0076]    # yaw rate
```

## Control Station Configuration

### File Location
Edit `src/ros_control_station/config/config.yaml`

### Vehicle List
```yaml
vehicles:
  - serial_number: "e6fa2a842d3ed36c"  # CPU serial number from /proc/cpuinfo
    name: "Robot 1"                    # Display name
    ip: "192.168.1.73"                # Robot IP address
  - serial_number: "0000000000000000"
    name: "Ghost Robot"
    ip: "192.168.1.74"
```

### Controller Settings
```yaml
Controller:
  max_speed: 1.5      # Maximum RPS (revolutions per second)
  center_pwm: 1500    # Servo center position (microseconds)
  pwm_range: 1000     # PWM range from center (±microseconds)
  max_turn: 0.4       # Maximum turn range (0.4 = 36 degrees)
```

## Extended Localization Configuration

### EKF Configuration
File: `src/ros_robot_controller/config/ekf.yaml`

This file configures the Extended Kalman Filter for sensor fusion:
- IMU and odometry data fusion
- Process and measurement noise parameters
- Sensor data source configuration

### SLAM Configuration
File: `src/ros_robot_controller/config/mapper_params_online_async.yaml`

This file configures the SLAM Toolbox:
- Map resolution and size
- Loop closure parameters
- Scan matching settings

## Parameter Tuning Guide

### IMU Calibration Process
1. Place robot on level surface
2. Run calibration: `ros2 run ros_robot_controller mpu6050_calibration`
3. Update bias values in config.yaml
4. Restart robot controller

### Vehicle Parameter Adjustment
- **wheel_radius**: Measure actual wheel radius
- **wheelbase**: Measure distance between front and rear axle centers
- **correction_factor**: Adjust based on actual vs. calculated speeds

### Controller Tuning
- **max_speed**: Adjust based on motor capabilities and safety requirements
- **max_turn**: Limit steering angle to prevent mechanical damage
- **pwm_range**: Match servo specifications

### Frequency Optimization
- **imu**: Higher for better orientation tracking (10-50 Hz)
- **all**: Balance between responsiveness and CPU load (5-20 Hz)
- **encoder**: Match motor encoder capabilities

## Troubleshooting Configuration Issues

### Common Problems
1. **Robot doesn't move**: Check motor directions and speed limits
2. **Steering incorrect**: Verify servo PWM center and range values
3. **IMU drift**: Recalibrate IMU bias values
4. **Poor odometry**: Check wheel radius and correction factor
5. **Vehicle selection fails**: Verify CPU serial numbers match

### Validation Commands
```bash
# Check current parameter values
ros2 param list /ros_robot_controller
ros2 param get /ros_robot_controller vehicle_data

# Monitor sensor data
ros2 topic echo /robot_control/imu
ros2 topic echo /odom
ros2 topic echo /robot_control/motors
``` 