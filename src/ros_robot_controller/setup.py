import os
from glob import glob
from setuptools import setup

package_name = 'ros_robot_controller'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob(os.path.join('launch', '*.*'))),
        (os.path.join('share', package_name, 'config'), glob(os.path.join('config', '*.yaml'))),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='ubuntu',
    maintainer_email='yuching.lin@outlook.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'ros_robot_controller = ros_robot_controller.ros_robot_controller_node:main',
            'motor_publisher = ros_robot_controller.motor_publisher:main',
            'odom_node = ros_robot_controller.ackermann_odom_node:main',
            'tf_publisher = ros_robot_controller.temp_tf_publisher:main',
            'mpu6050_calibration = ros_robot_controller.mpu6050_calibration:main',
        ],
    },
)
