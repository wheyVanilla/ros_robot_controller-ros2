# ROS2 Robot Controller Interface Documentation

## Overview

This document describes the interface specification for the ROS2 Robot Controller system, focusing on IMU, motor, and servo control capabilities through standardized ROS2 topics, services, and message types.

## Table of Contents

1. [System Architecture](#system-architecture)
2. [Topics](#topics)
3. [Services](#services)
4. [Message Types](#message-types)
5. [Service Types](#service-types)
6. [Usage Examples](#usage-examples)
7. [Multi-Robot Support](#multi-robot-support)
8. [Error Handling](#error-handling)

## System Architecture

The robot controller system consists of several key components:

- **Main Controller Node**: `ros_robot_controller_node.py`
- **Control Station**: `xbox_controller_node.py`
- **Odometry Node**: `ackermann_odom_node.py`
- **Hardware Interface**: `ros_robot_controller_sdk.py`

### Robot Identification

Each robot is uniquely identified by its CPU serial number, which is automatically read from `/proc/cpuinfo`. This ID is used for selective control in multi-robot scenarios.

## Topics

### Published Topics

#### Sensor Data
| Topic | Type | Description | Frequency |
|-------|------|-------------|-----------|
| `robot_control/imu_raw` | `sensor_msgs/Imu` | Raw IMU sensor data | Configurable |
| `robot_control/imu` | `sensor_msgs/Imu` | Bias-corrected IMU data | Configurable |
| `robot_control/motors` | `ros_robot_controller_msgs/MotorsState` | Current motor states | Based on comma |
| `robot_control/servo` | `ros_robot_controller_msgs/PWMServoState` | PWM servo position feedback | Based on command |

### Subscribed Topics

#### Control Commands
| Topic | Type | Description |
|-------|------|-------------|
| `robot_control/set_motor` | `ros_robot_controller_msgs/MotorsState` | Direct motor control commands |
| `robot_control/pwm_servo/set_state` | `ros_robot_controller_msgs/SetPWMServoState` | PWM servo control commands |


## Message Types

### Motor Control Messages

#### MotorState
```yaml
uint16 id      # Motor ID (1-4)
float64 rps    # Speed in rotations per second
```

#### MotorsState
```yaml
ros_robot_controller_msgs/MotorState[] data  # Array of motor states
```

### Servo Control Messages

#### PWMServoState
```yaml
uint16 id        # Servo ID
uint16 position  # PWM position (typically 500-2500)
int16 offset     # Position offset
```

#### SetPWMServoState
```yaml
ros_robot_controller_msgs/PWMServoState[] state  # Array of servo states
float64 duration                                  # Movement duration in seconds
```

### Query Command Messages

#### GetPWMServoCmd
```yaml
uint16 id           # Servo ID
uint8 get_position  # Request position (0/1)
uint8 get_offset    # Request offset (0/1)
```

## Service Types

### GetPWMServoState
```yaml
# Request
ros_robot_controller_msgs/GetPWMServoCmd[] cmd

# Response
bool success
ros_robot_controller_msgs/PWMServoState[] state
```

## Usage Examples

### Basic Motor Control

```python
import rclpy
from rclpy.node import Node
from ros_robot_controller_msgs.msg import MotorsState, MotorState

class MotorController(Node):
    def __init__(self):
        super().__init__('motor_controller')
        self.motor_pub = self.create_publisher(
            MotorsState, 
            'robot_control/set_motor', 
            10
        )
    
    def set_motor_speed(self, motor_id, speed_rps):
        msg = MotorsState()
        msg.data = [MotorState(id=motor_id, rps=speed_rps)]
        self.motor_pub.publish(msg)

# Usage
controller = MotorController()
controller.set_motor_speed(1, 0.5)  # Set motor 1 to 0.5 RPS
```

### PWM Servo Control

```python
from ros_robot_controller_msgs.msg import SetPWMServoState, PWMServoState

def set_pwm_servo_position(self, servo_id, position, duration=0.5):
    msg = SetPWMServoState()
    servo_state = PWMServoState()
    servo_state.id = servo_id
    servo_state.position = position
    msg.state = [servo_state]
    msg.duration = duration
    self.servo_pub.publish(msg)

# Usage
controller.set_pwm_servo_position(1, 1500)  # Center position
controller.set_pwm_servo_position(1, 2000)  # Full right
controller.set_pwm_servo_position(1, 1000)  # Full left
```

### IMU Data Monitoring

```python
from sensor_msgs.msg import Imu
import math

class IMUMonitor(Node):
    def __init__(self):
        super().__init__('imu_monitor')
        self.imu_sub = self.create_subscription(
            Imu,
            'robot_control/imu',
            self.imu_callback,
            10
        )
    
    def imu_callback(self, msg):
        # Access linear acceleration (m/s²)
        accel_x = msg.linear_acceleration.x
        accel_y = msg.linear_acceleration.y
        accel_z = msg.linear_acceleration.z
        
        # Access angular velocity (rad/s)
        gyro_x = msg.angular_velocity.x
        gyro_y = msg.angular_velocity.y
        gyro_z = msg.angular_velocity.z
        
        # Calculate acceleration magnitude
        accel_magnitude = math.sqrt(accel_x**2 + accel_y**2 + accel_z**2)
        
        self.get_logger().info(f'Accel: {accel_magnitude:.2f} m/s², Gyro Z: {math.degrees(gyro_z):.1f}°/s')
```

### Servo State Query

```python
from ros_robot_controller_msgs.srv import GetPWMServoState
from ros_robot_controller_msgs.msg import GetPWMServoCmd

class ServoMonitor(Node):
    def __init__(self):
        super().__init__('servo_monitor')
        self.servo_client = self.create_client(
            GetPWMServoState,
            'robot_control/pwm_servo/get_state'
        )
    
    async def get_servo_position(self, servo_id):
        request = GetPWMServoState.Request()
        cmd = GetPWMServoCmd()
        cmd.id = servo_id
        cmd.get_position = 1
        cmd.get_offset = 0
        request.cmd = [cmd]
        
        future = self.servo_client.call_async(request)
        response = await future
        
        if response.success and response.state:
            return response.state[0].position
        return None
```




