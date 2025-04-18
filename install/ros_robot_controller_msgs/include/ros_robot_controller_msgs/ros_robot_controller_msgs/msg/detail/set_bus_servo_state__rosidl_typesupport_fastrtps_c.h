// generated from rosidl_typesupport_fastrtps_c/resource/idl__rosidl_typesupport_fastrtps_c.h.em
// with input from ros_robot_controller_msgs:msg/SetBusServoState.idl
// generated code does not contain a copyright notice
#ifndef ROS_ROBOT_CONTROLLER_MSGS__MSG__DETAIL__SET_BUS_SERVO_STATE__ROSIDL_TYPESUPPORT_FASTRTPS_C_H_
#define ROS_ROBOT_CONTROLLER_MSGS__MSG__DETAIL__SET_BUS_SERVO_STATE__ROSIDL_TYPESUPPORT_FASTRTPS_C_H_


#include <stddef.h>
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "rosidl_typesupport_interface/macros.h"
#include "ros_robot_controller_msgs/msg/rosidl_typesupport_fastrtps_c__visibility_control.h"
#include "ros_robot_controller_msgs/msg/detail/set_bus_servo_state__struct.h"
#include "fastcdr/Cdr.h"

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_ros_robot_controller_msgs
bool cdr_serialize_ros_robot_controller_msgs__msg__SetBusServoState(
  const ros_robot_controller_msgs__msg__SetBusServoState * ros_message,
  eprosima::fastcdr::Cdr & cdr);

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_ros_robot_controller_msgs
bool cdr_deserialize_ros_robot_controller_msgs__msg__SetBusServoState(
  eprosima::fastcdr::Cdr &,
  ros_robot_controller_msgs__msg__SetBusServoState * ros_message);

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_ros_robot_controller_msgs
size_t get_serialized_size_ros_robot_controller_msgs__msg__SetBusServoState(
  const void * untyped_ros_message,
  size_t current_alignment);

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_ros_robot_controller_msgs
size_t max_serialized_size_ros_robot_controller_msgs__msg__SetBusServoState(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_ros_robot_controller_msgs
bool cdr_serialize_key_ros_robot_controller_msgs__msg__SetBusServoState(
  const ros_robot_controller_msgs__msg__SetBusServoState * ros_message,
  eprosima::fastcdr::Cdr & cdr);

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_ros_robot_controller_msgs
size_t get_serialized_size_key_ros_robot_controller_msgs__msg__SetBusServoState(
  const void * untyped_ros_message,
  size_t current_alignment);

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_ros_robot_controller_msgs
size_t max_serialized_size_key_ros_robot_controller_msgs__msg__SetBusServoState(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_ros_robot_controller_msgs
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, ros_robot_controller_msgs, msg, SetBusServoState)();

#ifdef __cplusplus
}
#endif

#endif  // ROS_ROBOT_CONTROLLER_MSGS__MSG__DETAIL__SET_BUS_SERVO_STATE__ROSIDL_TYPESUPPORT_FASTRTPS_C_H_
