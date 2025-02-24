import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Joy
from std_msgs.msg import String
import tkinter as tk
from threading import Thread
import time
import os
import yaml

class VehicleControlStation(Node):
    def __init__(self, app):
        super().__init__('vehicle_control_station')
        self.app = app
        self.last_input_time = time.time()
        self.input_delay = 0.3

        # Declare config path
        self.declare_parameter('config_path','src/ros_control_station/config/config.yaml')
        config_path = self.get_parameter('config_path').value

        # Load config
        self.vehicles = self.load_config(config_path)
        self.selected_vehicle = None

        self.subscription = self.create_subscription(
            Joy,
            'joy',
            self.joy_callback,
            10)
        self.publisher_selected_vehicle = self.create_publisher(String,'manual_control/selection',10)
        
        self.get_logger().info(f"Load {len(self.vehicles)} small bu bu")

        self.gui_setup()

    def load_config(self,path):
        try:
            abs_path = os.path.abspath(path)
            with open(abs_path,'r') as file:
                config = yaml.safe_load(file)
            return config['vehicles']

        except Exception as e:
            self.get_logger().error(f"Failed to load config: {e}")
            return []
        

    def gui_setup(self):

        self.selected_value = tk.IntVar(value=0)
        self.radio_buttons = []
        self.radio_buttons.extend(tk.Radiobutton(self.app, text=f"{self.vehicles[i]['name']}", variable=self.selected_value, value=i, command=self.update_color) for i in range(len(self.vehicles)))        
        self.radio_buttons.append(tk.Radiobutton(self.app, text=f"None", variable=self.selected_value, value=len(self.vehicles), command=self.update_color))
        
        for rb in self.radio_buttons:
            rb.pack(anchor=tk.W)
            rb.config(bg="#b9b9b9")
        

    def update_color(self):
        # Update GUI elements safely within the main thread
        for rb in self.radio_buttons:
            if self.selected_value.get() == rb['value']:
                rb.config(foreground='white')
            else:
                rb.config(foreground='black')
     
    # use right joystick to navigate and A button to select
    def joy_callback(self, msg):
        current_time = time.time()
        if (current_time - self.last_input_time) > self.input_delay:
            if msg.axes[4]> 0.7:
                self.nav_button(-1)
                self.last_input_time = current_time
            elif msg.axes[4] < -0.7:
                self.nav_button(1)
                self.last_input_time = current_time

            if msg.buttons[0]==1:
                self.select_button()
                self.last_input_time = current_time
    
    def nav_button(self,direction):
        new_index = (self.selected_value.get() + direction) % len(self.radio_buttons)
        self.selected_value.set(new_index)
        self.app.after(0, self.update_color)  # Update the GUI safely

    def select_button(self):
        # Log or process the selected button
        option = self.selected_value.get()
        msg = String()
        if option is len(self.vehicles):
            msg.data = 'none'
            self.get_logger().info(f'Stop Manual Control')
        else:
            self.get_logger().info(f'Selected: {self.vehicles[option]['name']}')
            msg.data = self.vehicles[option]['serial_number']
        self.publisher_selected_vehicle.publish(msg)     
        for rb in self.radio_buttons:
            if self.selected_value.get() == rb['value']:
                rb.config(bg='#5fbc20')
            else:
                rb.config(bg='#b9b9b9')
        

def main(args=None):
    rclpy.init(args=args)
    app = tk.Tk()
    app.title("Vehicle Selection")

    gui_node = VehicleControlStation(app)

    # Run ROS 2 node in a separate thread
    thread = Thread(target=lambda: rclpy.spin(gui_node))
    thread.start()

    app.mainloop()  # Keep the mainloop in the main thread

    gui_node.destroy_node()
    rclpy.shutdown()
    thread.join()

if __name__ == '__main__':
    main()