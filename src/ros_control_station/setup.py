from setuptools import setup
import os
from glob import glob

package_name = 'ros_control_station'

setup(
    name=package_name,
    version='0.0.1',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), 
         glob(os.path.join('launch', '*launch.[pxy][yma]*')))
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='yc',
    maintainer_email='yuching.lin@outlook.com',
    description='Control station',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'xbox_controller = ros_control_station.xbox_controller_node:main',
            'vehicle_control_station = ros_control_station.vehicle_selection_node:main',
        ],
    },
)
