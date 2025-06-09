#!/bin/bash

# === Settings ===
if [ "$#" -eq 0 ]; then
    echo "Error: No robot hosts specified. Please provide at least one."
    echo "Usage: $0 <robot_host1> [robot_host2]..."
    exit 1
fi
ROBOT_HOSTS=("$@")
WORKSPACE_DIR=~/Documents/ROS2/ros_robot_controller-ros2
ARCHIVE_NAME=robot_ws.tar.gz
REMOTE_HOME=/home/robot/ros2

# Check if SUDO_PASS is set
if [ -z "$SUDO_PASS" ]; then
    echo "Error: SUDO_PASS environment variable is not set"
    echo "Please set it first by running:"
    echo "export SUDO_PASS='your_robot_sudo_password'"
    exit 1
fi

# === Step 1: Package source files ===
echo "[*] Creating source archive..."
cd $WORKSPACE_DIR
tar czf $ARCHIVE_NAME src/

# === Step 2: Deploy to each robot ===
for HOST in "${ROBOT_HOSTS[@]}"; do
    echo "[*] Deploying to $HOST..."

    # Copy source files
    scp $WORKSPACE_DIR/$ARCHIVE_NAME robot@$HOST:$REMOTE_HOME/

    # Remote setup commands
    ssh robot@$HOST bash <<EOF
        cd $REMOTE_HOME
        rm -rf src  # Clean old source files
        tar xzf $ARCHIVE_NAME
        
        # Build on robot
        echo "[*] Building on robot..."
        source /opt/ros/jazzy/setup.bash
        colcon build || { echo "Build failed on robot"; exit 1; }
        
        # Deploy start_robot.sh
        echo "[*] Deploying start_robot.sh..."
        cp $REMOTE_HOME/src/ros_robot_controller/scripts/start_robot.sh $REMOTE_HOME/
        chmod +x $REMOTE_HOME/start_robot.sh
        
        # Deploy systemd service
        echo "[*] Deploying systemd service..."
        echo "$SUDO_PASS" | sudo -S cp $REMOTE_HOME/src/ros_robot_controller/scripts/robot_launcher.service /etc/systemd/system/
        echo "$SUDO_PASS" | sudo -S systemctl daemon-reload
        echo "$SUDO_PASS" | sudo -S systemctl enable robot_launcher.service
        
        # Restart service
        echo "$SUDO_PASS" | sudo -S systemctl restart robot_launcher.service
EOF

    echo "[✓] Done with $HOST"
done

echo "[✔] Deployment complete."
