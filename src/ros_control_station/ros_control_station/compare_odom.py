import rosbag2_py
from rclpy.serialization import deserialize_message
from rosidl_runtime_py.utilities import get_message
import matplotlib.pyplot as plt
import numpy as np

# Initialize dictionaries to store data
odom_data = {'time': [], 'x': [], 'y': [], 'theta': []}
filtered_data = {'time': [], 'x': [], 'y': [], 'theta': []}

# Open the bag file (changed to mcap format)
storage_options = rosbag2_py.StorageOptions(uri='/home/yc/Documents/ROS2/ros_robot_controller-ros2/src/ros_control_station/ros_control_station/compare_odom/compare_odom_0.mcap', storage_id='mcap')
converter_options = rosbag2_py.ConverterOptions(input_serialization_format='cdr', output_serialization_format='cdr')
reader = rosbag2_py.SequentialReader()
reader.open(storage_options, converter_options)

# Get the Odometry message type
odom_msg_type = get_message('nav_msgs/msg/Odometry')

# Read messages from the bag
while reader.has_next():
    (topic, data, timestamp) = reader.read_next()
    msg = deserialize_message(data, odom_msg_type)
    
    # Extract position (x, y) and orientation (theta from quaternion)
    x = msg.pose.pose.position.x
    y = msg.pose.pose.position.y
    q = msg.pose.pose.orientation
    theta = np.arctan2(2.0 * (q.w * q.z + q.x * q.y), 1.0 - 2.0 * (q.y * q.y + q.z * q.z))
    time_ns = timestamp

    # Store data based on topic
    if topic == '/odom':
        odom_data['time'].append(time_ns)
        odom_data['x'].append(x)
        odom_data['y'].append(y)
        odom_data['theta'].append(theta)
    elif topic == '/odometry/filtered':
        filtered_data['time'].append(time_ns)
        filtered_data['x'].append(x)
        filtered_data['y'].append(y)
        filtered_data['theta'].append(theta)

del reader  # Close the reader

# Convert timestamps to seconds relative to the start
odom_time = [(t - odom_data['time'][0]) / 1e9 for t in odom_data['time']]
filtered_time = [(t - filtered_data['time'][0]) / 1e9 for t in filtered_data['time']]

# Interpolate filtered data to match odom timestamps
filtered_x_interp = np.interp(odom_time, filtered_time, filtered_data['x'])
filtered_y_interp = np.interp(odom_time, filtered_time, filtered_data['y'])
filtered_theta_interp = np.interp(odom_time, filtered_time, filtered_data['theta'])

# Calculate differences
diff_x = np.array(odom_data['x']) - filtered_x_interp
diff_y = np.array(odom_data['y']) - filtered_y_interp
diff_theta = np.array(odom_data['theta']) - filtered_theta_interp

# Visualize
plt.figure(figsize=(12, 8))

plt.subplot(3, 1, 1)
plt.plot(odom_time, odom_data['x'], label='/odom x')
plt.plot(odom_time, filtered_x_interp, label='/odometry/filtered x')
plt.title('X Position Comparison')
plt.xlabel('Time (s)')
plt.ylabel('X (m)')
plt.legend()

plt.subplot(3, 1, 2)
plt.plot(odom_time, odom_data['y'], label='/odom y')
plt.plot(odom_time, filtered_y_interp, label='/odometry/filtered y')
plt.title('Y Position Comparison')
plt.xlabel('Time (s)')
plt.ylabel('Y (m)')
plt.legend()

plt.subplot(3, 1, 3)
plt.plot(odom_time, odom_data['theta'], label='/odom theta')
plt.plot(odom_time, filtered_theta_interp, label='/odometry/filtered theta')
plt.title('Yaw Comparison')
plt.xlabel('Time (s)')
plt.ylabel('Theta (rad)')
plt.legend()

plt.tight_layout()
plt.show()

# Print statistics
print("X Difference - Mean:", np.mean(diff_x), "Std Dev:", np.std(diff_x))
print("Y Difference - Mean:", np.mean(diff_y), "Std Dev:", np.std(diff_y))
print("Theta Difference - Mean:", np.mean(diff_theta), "Std Dev:", np.std(diff_theta))