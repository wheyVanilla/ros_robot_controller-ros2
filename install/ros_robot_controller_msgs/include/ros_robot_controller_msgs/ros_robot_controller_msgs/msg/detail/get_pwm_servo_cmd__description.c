// generated from rosidl_generator_c/resource/idl__description.c.em
// with input from ros_robot_controller_msgs:msg/GetPWMServoCmd.idl
// generated code does not contain a copyright notice

#include "ros_robot_controller_msgs/msg/detail/get_pwm_servo_cmd__functions.h"

ROSIDL_GENERATOR_C_PUBLIC_ros_robot_controller_msgs
const rosidl_type_hash_t *
ros_robot_controller_msgs__msg__GetPWMServoCmd__get_type_hash(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_type_hash_t hash = {1, {
      0xe2, 0x7a, 0xb0, 0x7b, 0x63, 0x3d, 0x91, 0xfb,
      0x42, 0x35, 0x27, 0xa6, 0xac, 0xd4, 0xa2, 0x1b,
      0xde, 0x8b, 0x10, 0xd4, 0x86, 0xfe, 0xb7, 0x6a,
      0x96, 0x1c, 0x4a, 0x5b, 0x0f, 0x74, 0xdb, 0x39,
    }};
  return &hash;
}

#include <assert.h>
#include <string.h>

// Include directives for referenced types

// Hashes for external referenced types
#ifndef NDEBUG
#endif

static char ros_robot_controller_msgs__msg__GetPWMServoCmd__TYPE_NAME[] = "ros_robot_controller_msgs/msg/GetPWMServoCmd";

// Define type names, field names, and default values
static char ros_robot_controller_msgs__msg__GetPWMServoCmd__FIELD_NAME__id[] = "id";
static char ros_robot_controller_msgs__msg__GetPWMServoCmd__FIELD_NAME__get_position[] = "get_position";
static char ros_robot_controller_msgs__msg__GetPWMServoCmd__FIELD_NAME__get_offset[] = "get_offset";

static rosidl_runtime_c__type_description__Field ros_robot_controller_msgs__msg__GetPWMServoCmd__FIELDS[] = {
  {
    {ros_robot_controller_msgs__msg__GetPWMServoCmd__FIELD_NAME__id, 2, 2},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_UINT16,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {ros_robot_controller_msgs__msg__GetPWMServoCmd__FIELD_NAME__get_position, 12, 12},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_UINT8,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {ros_robot_controller_msgs__msg__GetPWMServoCmd__FIELD_NAME__get_offset, 10, 10},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_UINT8,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
};

const rosidl_runtime_c__type_description__TypeDescription *
ros_robot_controller_msgs__msg__GetPWMServoCmd__get_type_description(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static bool constructed = false;
  static const rosidl_runtime_c__type_description__TypeDescription description = {
    {
      {ros_robot_controller_msgs__msg__GetPWMServoCmd__TYPE_NAME, 44, 44},
      {ros_robot_controller_msgs__msg__GetPWMServoCmd__FIELDS, 3, 3},
    },
    {NULL, 0, 0},
  };
  if (!constructed) {
    constructed = true;
  }
  return &description;
}

static char toplevel_type_raw_source[] =
  "uint16 id\n"
  "uint8 get_position\n"
  "uint8 get_offset";

static char msg_encoding[] = "msg";

// Define all individual source functions

const rosidl_runtime_c__type_description__TypeSource *
ros_robot_controller_msgs__msg__GetPWMServoCmd__get_individual_type_description_source(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static const rosidl_runtime_c__type_description__TypeSource source = {
    {ros_robot_controller_msgs__msg__GetPWMServoCmd__TYPE_NAME, 44, 44},
    {msg_encoding, 3, 3},
    {toplevel_type_raw_source, 46, 46},
  };
  return &source;
}

const rosidl_runtime_c__type_description__TypeSource__Sequence *
ros_robot_controller_msgs__msg__GetPWMServoCmd__get_type_description_sources(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_runtime_c__type_description__TypeSource sources[1];
  static const rosidl_runtime_c__type_description__TypeSource__Sequence source_sequence = {sources, 1, 1};
  static bool constructed = false;
  if (!constructed) {
    sources[0] = *ros_robot_controller_msgs__msg__GetPWMServoCmd__get_individual_type_description_source(NULL),
    constructed = true;
  }
  return &source_sequence;
}
