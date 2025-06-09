#!/usr/bin/env bash
echo "[*] Starting robot controller..."

echo "[*] Sourcing ROS2..."
source /opt/ros/jazzy/setup.bash

echo "[*] Sourcing workspace..."
source ~/ros2/install/setup.bash

echo "[*] Launching controller in foreground..."
exec ros2 launch ros_robot_controller slam_localization.launch.py
