import yaml
import rclpy.logging
import os
import math
from geometry_msgs.msg import Quaternion

def load_config(node, config_key='ros_robot_controller_node', config_path=None,config_path_param='config_path', default_path='src/ros_robot_controller/config/config.yaml'):
    logger = node.get_logger()
    
    if config_path is None:
        node.declare_parameter(config_path_param, default_path)
        config_path = node.get_parameter(config_path_param).get_parameter_value().string_value
        
    try:
        abs_path = os.path.abspath(config_path)
        with open(abs_path, 'r') as file:
            config = yaml.safe_load(file) or {}
        logger.info(f"Loaded config from {abs_path} with key '{config_key}'")
        return config.get(config_key, {})
    except FileNotFoundError:
        logger.error(f"Config file not found at {config_path}")
        return {}
    except Exception as e:
        logger.error(f"Failed to load config: {e}")
        return {}
    
def normalize_angle(angle):
    """
    Normalize an angle to the range [-pi, pi].

    Args:
        angle (float): Angle in radians.

    Returns:
        float: Normalized angle in radians.
    """
    while angle > math.pi:
        angle -= 2 * math.pi
    while angle < -math.pi:
        angle += 2 * math.pi
    return angle

def pwm_to_angle(pwm, center_pwm, pwm_range, max_angle):
    """
    Convert PWM value to an angle (radians) based on center and range.

    Args:
        pwm (int): PWM value in microseconds.
        center_pwm (int): Center PWM value in microseconds.
        pwm_range (int): PWM range from center (±microseconds).
        max_angle (float): Maximum angle in radians.

    Returns:
        float: Angle in radians, clamped to [-max_angle, max_angle].
    """
    pwm_offset = pwm - center_pwm
    angle_normalized = pwm_offset / pwm_range  # -1 to 1
    angle = angle_normalized * max_angle
    return max(min(angle, max_angle), -max_angle)

def quaternion_from_yaw(yaw):
    """
    Convert a yaw angle (radians) to a quaternion.

    Args:
        yaw (float): Yaw angle in radians.

    Returns:
        geometry_msgs.msg.Quaternion: Quaternion representation.
    """
    q = Quaternion()
    q.x = 0.0
    q.y = 0.0
    q.z = math.sin(yaw / 2.0)
    q.w = math.cos(yaw / 2.0)
    return q