#!/usr/bin/env python3
# encoding: utf-8
# @Author: Aiden
# @Date: 2023/08/28
# stm32 ros2 package
import math
import rclpy
import signal
import gpiod

from rclpy.node import Node
from std_msgs.msg import UInt16
from std_msgs.msg import String
from sensor_msgs.msg import Imu, Joy
from ros_robot_controller.ros_robot_controller_sdk import Board
from ros_robot_controller_msgs.srv import GetBusServoState, GetPWMServoState
from ros_robot_controller_msgs.msg import ButtonState, BuzzerState, LedState, MotorsState, BusServoState, PWMServoState, SetBusServoState, SetPWMServoState, Sbus

class RosRobotController(Node):
    gravity = 9.80665
    def __init__(self, name):
        rclpy.init()
        super().__init__(name)
        
        self.manaul_control_flag = False
        self.board = Board()
        self.board.enable_reception()
        signal.signal(signal.SIGINT, self.shutdown)

        # Read CPU serial number as vehicle ID
        self.vehicle_id = self.get_cpu_serial()
        self.get_logger().info(f"Vehicle ID: {self.vehicle_id}")

        # GPIO setup
        self.led_pin = 17
        self.chip = gpiod.Chip('gpiochip4')
        self.line = self.chip.get_line(self.led_pin)
        self.line.request(consumer='ros_robot_controller', type=gpiod.LINE_REQ_DIR_OUT)


        # initialize
        self.declare_parameter('imu_frame', 'imu_link')
        self.IMU_FRAME = self.get_parameter('imu_frame').value

        self.imu_pub = self.create_publisher(Imu, '~/imu_raw', 1)
        self.joy_pub = self.create_publisher(Joy, '~/joy', 1)
        self.sbus_pub = self.create_publisher(Sbus, '~/sbus', 1)
        self.button_pub = self.create_publisher(ButtonState, '~/button', 1)
        self.battery_pub = self.create_publisher(UInt16, '~/battery', 1)
        self.create_subscription(LedState, '~/set_led', self.set_led_state, 1)
        self.create_subscription(BuzzerState, '~/set_buzzer', self.set_buzzer_state, 1)
        self.create_subscription(MotorsState, '~/set_motor', self.set_motor_state, 1)
        self.create_subscription(SetBusServoState, '~/bus_servo/set_state', self.set_bus_servo_state, 1)
        self.create_subscription(String,'manual_control/selection',self.set_manaul_control,10)
        self.create_subscription(MotorsState,'manual_control/set_motor', self.set_manual_motor_state, 1)
        self.create_subscription(SetPWMServoState,'manual_control/pwn_servo_set_state', self.set_manual_pwn_servo_state, 1)
        self.create_service(GetBusServoState, '~/bus_servo/get_state', self.get_bus_servo_state)
        self.create_subscription(SetPWMServoState, '~/pwm_servo/set_state', self.set_pwm_servo_state, 1)
        self.create_service(GetPWMServoState, '~/pwm_servo/get_state', self.get_pwm_servo_state)

        self.clock = self.get_clock()
        self.create_timer(1.0/100.0, self.pub_callback)
        self.get_logger().info('\033[1;32m%s\033[0m' % 'start')

    def shutdown(self, signum, frame):
        self.get_logger().info('\033[1;32m%s\033[0m' % 'shutdown')
        rclpy.shutdown()

    def pub_callback(self):
        self.pub_button_data(self.button_pub)
        self.pub_joy_data(self.joy_pub)
        self.pub_imu_data(self.imu_pub)
        self.pub_sbus_data(self.sbus_pub)
        self.pub_battery_data(self.battery_pub)

    def set_led_state(self, msg):
        self.board.set_led(msg.on_time, msg.off_time, msg.repeat, msg.id)

    def set_buzzer_state(self, msg):
        self.board.set_buzzer(msg.freq, msg.on_time, msg.off_time, msg.repeat)

    def set_motor_state(self, msg):
        data = []
        for i in msg.data:
            data.extend([[i.id, i.rps]])
        self.board.set_motor_speed(data)

    def set_pwm_servo_state(self, msg):
        data = []

        print(msg)

        for i in msg.state:
            if i.id and i.position:
                    data.extend([i.id, i.position])
                    self.board.pwm_servo_set_position(msg.duration, data)
            if i.id and i.offset:
                    self.board.pwm_servo_set_offset(i.id, i.offset)
            
    def get_pwm_servo_state(self, msg, response):
        states = []
        print("======================")
        print(msg)
        for i in msg.cmd:
            data = PWMServoState()
            if i.get_position:
                state = self.board.pwm_servo_read_position(i.id)
                print(f"state {state}")
                if state is not None:
                    data.position = state
            if i.get_offset:
                state = self.board.pwm_servo_read_offset(i.id)
                if state is not None:
                    data.offset = state
            states.append(data)
        response.state = states
        response.success = True
        return response

    def set_bus_servo_state(self, msg):
        data = []
        servo_id = []
        for i in msg.state:
            if i.present_id:
                if i.present_id[0]:
                    if i.target_id:
                        if i.target_id[0]:
                            self.board.bus_servo_set_id(i.present_id[1], i.target_id[1])
                    if i.position:
                        if i.position[0]:
                            data.extend([[i.present_id[1], i.position[1]]])
                    if i.offset:
                        if i.offset[0]:
                            self.board.bus_servo_set_offset(i.present_id[1], i.offset[1])
                    if i.position_limit:
                        if i.position_limit[0]:
                            self.board.bus_servo_set_angle_limit(i.present_id[1], i.position_limit[1:])
                    if i.voltage_limit:
                        if i.voltage_limit[0]:
                            self.board.bus_servo_set_vin_limit(i.present_id[1], i.voltage_limit[1:])
                    if i.max_temperature_limit:
                        if i.max_temperature_limit[0]:
                            self.board.bus_servo_set_temp_limit(i.present_id[1], i.max_temperature_limit[1])
                    if i.enable_torque:
                        if i.enable_torque[0]:
                            self.board.bus_servo_enable_torque(i.present_id[1], i.enable_torque[1])
                    if i.save_offset:
                        if i.save_offset[0]:
                            self.board.bus_servo_save_offset(i.present_id[1])
                    if i.stop:
                        if i.stop[0]:
                            servo_id.append(i.present_id[1])
        if data != []:
            self.board.bus_servo_set_position(msg.duration, data)
        if servo_id != []:    
            self.board.bus_servo_stop(servo_id)

    def get_bus_servo_state(self, request, response):
        states = []
        for i in request.cmd:
            data = BusServoState()
            if i.get_id:
                state = self.board.bus_servo_read_id(i.id)
                if state is not None:
                    i.id = state[0]
                    data.present_id = state
            if i.get_position:
                state = self.board.bus_servo_read_position(i.id)
                if state is not None:
                    data.position = state
            if i.get_offset:
                state = self.board.bus_servo_read_offset(i.id)
                if state is not None:
                    data.offset = state
            if i.get_voltage:
                state = self.board.bus_servo_read_voltage(i.id)
                if state is not None:
                    data.voltage = state
            if i.get_temperature:
                state = self.board.bus_servo_read_temp(i.id)
                if state is not None:
                    data.temperature = state
            if i.get_position_limit:
                state = self.board.bus_servo_read_angle_limit(i.id)
                if state is not None:
                    data.position_limit = state
            if i.get_voltage_limit:
                state = self.board.bus_servo_read_vin_limit(i.id)
                if state is not None:
                    data.voltage_limit = state
            if i.get_max_temperature_limit:
                state = self.board.bus_servo_read_temp_limit(i.id)
                if state is not None:
                    data.max_temperature_limit = state
            if i.get_torque_state:
                state = self.board.bus_servo_read_torque(i.id)
                if state is not None:
                    data.enable_torque = state
            states.append(data)
        response.state = states
        response.success = True
        return response

    def pub_battery_data(self, pub):
        data = self.board.get_battery()
        if data is not None:
            msg = UInt16()
            msg.data = data
            pub.publish(msg)

    def pub_button_data(self, pub):
        data = self.board.get_button()
        if data is not None:
            msg = ButtonState()
            msg.id = data[0]
            msg.state = data[1]
            pub.publish(msg)

    def pub_joy_data(self, pub):
        data = self.board.get_gamepad()
        if data is not None:
            msg = Joy()
            msg.axes = data[0]
            msg.buttons = data[1]
            msg.header.stamp = self.clock.now().to_msg()
            pub.publish(msg)

    def pub_sbus_data(self, pub):
        data = self.board.get_sbus()
        if data is not None:
            msg = Sbus()
            msg.channel = data
            msg.header.stamp = self.clock.now().to_msg()
            pub.publish(msg)

    def pub_imu_data(self, pub):
        data = self.board.get_imu()
        if data is not None:
            ax, ay, az, gx, gy, gz = data
            msg = Imu()
            msg.header.frame_id = self.IMU_FRAME
            msg.header.stamp = self.clock.now().to_msg()

            msg.orientation.w = 0.0
            msg.orientation.x = 0.0
            msg.orientation.y = 0.0
            msg.orientation.z = 0.0

            msg.linear_acceleration.x = ax * self.gravity
            msg.linear_acceleration.y = ay * self.gravity
            msg.linear_acceleration.z = az * self.gravity

            msg.angular_velocity.x = math.radians(gx)
            msg.angular_velocity.y = math.radians(gy)
            msg.angular_velocity.z = math.radians(gz)

            msg.orientation_covariance = [0.01, 0.0, 0.0, 0.0, 0.01, 0.0, 0.0, 0.0, 0.01]
            msg.angular_velocity_covariance = [0.01, 0.0, 0.0, 0.0, 0.01, 0.0, 0.0, 0.0, 0.01]
            msg.linear_acceleration_covariance = [0.0004, 0.0, 0.0, 0.0, 0.0004, 0.0, 0.0, 0.0, 0.004]
            pub.publish(msg)

    def set_manaul_control(self, msg):
        request_id = msg.data
        self.get_logger().info(f"Received control request for ID: {request_id}")
        if request_id == self.vehicle_id:
            self.get_logger().info("ID matches. Lighting up the LED.")
            self.manaul_control_flag = True
            self.line.set_value(1)
        else:
            self.get_logger().info("ID does not match. Turning off the LED.")
            self.manaul_control_flag = False
            self.line.set_value(0)

    def set_manual_motor_state(self, msg):
        if self.manaul_control_flag:
            self.set_motor_state(msg)

    def set_manual_pwn_servo_state(self, msg):
        if self.manaul_control_flag:
            self.set_pwm_servo_state(msg)
def main():
    node = RosRobotController('ros_robot_controller')
    rclpy.spin(node)
    self.line.release()
    node.destroy_node()
    rclpy.shutdown()
                           
if __name__ == '__main__':
    main()

