#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import RPi.GPIO as GPIO

class ManualController(Node):
    def __init__(self):
        super().__init__('manual_controller')

        # Read CPU serial number as vehicle ID
        self.vehicle_id = self.get_cpu_serial()
        self.get_logger().info(f"Vehicle ID: {self.vehicle_id}")

        # GPIO setup
        self.led_pin = 17
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.led_pin, GPIO.OUT)
        GPIO.output(self.led_pin, GPIO.LOW)

        # Subscriber for control requests
        self.control_sub = self.create_subscription(
            String,
            'manual_control/selection',
            self.control_callback,
            10
        )

    def get_cpu_serial(self):
        """Reads the CPU serial number of the Raspberry Pi."""
        try:
            with open('/proc/cpuinfo', 'r') as f:
                for line in f:
                    if line.startswith('Serial'):
                        return line.strip().split(': ')[1]
        except Exception as e:
            self.get_logger().error(f"Failed to read CPU serial number: {e}")
            return "UNKNOWN"

    def control_callback(self, msg):
        """Handles control requests and lights up the LED if the ID matches."""
        request_id = msg.data
        self.get_logger().info(f"Received control request for ID: {request_id}")

        if request_id == self.vehicle_id:
            self.get_logger().info("ID matches. Lighting up the LED.")
            GPIO.output(self.led_pin, GPIO.HIGH)
        else:
            self.get_logger().info("ID does not match. Turning off the LED.")
            GPIO.output(self.led_pin, GPIO.LOW)

    def destroy_node(self):
        """Cleanup GPIO on shutdown."""
        GPIO.cleanup()
        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    node = ManualController()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
