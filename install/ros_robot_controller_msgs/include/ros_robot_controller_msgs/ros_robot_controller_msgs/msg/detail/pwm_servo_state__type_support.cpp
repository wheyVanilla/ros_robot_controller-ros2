// generated from rosidl_typesupport_introspection_cpp/resource/idl__type_support.cpp.em
// with input from ros_robot_controller_msgs:msg/PWMServoState.idl
// generated code does not contain a copyright notice

#include "array"
#include "cstddef"
#include "string"
#include "vector"
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "rosidl_typesupport_cpp/message_type_support.hpp"
#include "rosidl_typesupport_interface/macros.h"
#include "ros_robot_controller_msgs/msg/detail/pwm_servo_state__functions.h"
#include "ros_robot_controller_msgs/msg/detail/pwm_servo_state__struct.hpp"
#include "rosidl_typesupport_introspection_cpp/field_types.hpp"
#include "rosidl_typesupport_introspection_cpp/identifier.hpp"
#include "rosidl_typesupport_introspection_cpp/message_introspection.hpp"
#include "rosidl_typesupport_introspection_cpp/message_type_support_decl.hpp"
#include "rosidl_typesupport_introspection_cpp/visibility_control.h"

namespace ros_robot_controller_msgs
{

namespace msg
{

namespace rosidl_typesupport_introspection_cpp
{

void PWMServoState_init_function(
  void * message_memory, rosidl_runtime_cpp::MessageInitialization _init)
{
  new (message_memory) ros_robot_controller_msgs::msg::PWMServoState(_init);
}

void PWMServoState_fini_function(void * message_memory)
{
  auto typed_message = static_cast<ros_robot_controller_msgs::msg::PWMServoState *>(message_memory);
  typed_message->~PWMServoState();
}

static const ::rosidl_typesupport_introspection_cpp::MessageMember PWMServoState_message_member_array[3] = {
  {
    "id",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_UINT16,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(ros_robot_controller_msgs::msg::PWMServoState, id),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "position",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_UINT16,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(ros_robot_controller_msgs::msg::PWMServoState, position),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "offset",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_INT16,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(ros_robot_controller_msgs::msg::PWMServoState, offset),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  }
};

static const ::rosidl_typesupport_introspection_cpp::MessageMembers PWMServoState_message_members = {
  "ros_robot_controller_msgs::msg",  // message namespace
  "PWMServoState",  // message name
  3,  // number of fields
  sizeof(ros_robot_controller_msgs::msg::PWMServoState),
  false,  // has_any_key_member_
  PWMServoState_message_member_array,  // message members
  PWMServoState_init_function,  // function to initialize message memory (memory has to be allocated)
  PWMServoState_fini_function  // function to terminate message instance (will not free memory)
};

static const rosidl_message_type_support_t PWMServoState_message_type_support_handle = {
  ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  &PWMServoState_message_members,
  get_message_typesupport_handle_function,
  &ros_robot_controller_msgs__msg__PWMServoState__get_type_hash,
  &ros_robot_controller_msgs__msg__PWMServoState__get_type_description,
  &ros_robot_controller_msgs__msg__PWMServoState__get_type_description_sources,
};

}  // namespace rosidl_typesupport_introspection_cpp

}  // namespace msg

}  // namespace ros_robot_controller_msgs


namespace rosidl_typesupport_introspection_cpp
{

template<>
ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<ros_robot_controller_msgs::msg::PWMServoState>()
{
  return &::ros_robot_controller_msgs::msg::rosidl_typesupport_introspection_cpp::PWMServoState_message_type_support_handle;
}

}  // namespace rosidl_typesupport_introspection_cpp

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, ros_robot_controller_msgs, msg, PWMServoState)() {
  return &::ros_robot_controller_msgs::msg::rosidl_typesupport_introspection_cpp::PWMServoState_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif
