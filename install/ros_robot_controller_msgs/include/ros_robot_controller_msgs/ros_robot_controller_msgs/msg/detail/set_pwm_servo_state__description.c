// generated from rosidl_generator_c/resource/idl__description.c.em
// with input from ros_robot_controller_msgs:msg/SetPWMServoState.idl
// generated code does not contain a copyright notice

#include "ros_robot_controller_msgs/msg/detail/set_pwm_servo_state__functions.h"

ROSIDL_GENERATOR_C_PUBLIC_ros_robot_controller_msgs
const rosidl_type_hash_t *
ros_robot_controller_msgs__msg__SetPWMServoState__get_type_hash(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_type_hash_t hash = {1, {
      0x2e, 0x2a, 0x94, 0x60, 0x7f, 0x7e, 0x3d, 0x49,
      0x17, 0xcf, 0x87, 0x71, 0x8b, 0x9a, 0xb1, 0x45,
      0x98, 0x9a, 0x0c, 0x92, 0xed, 0x75, 0xc1, 0xce,
      0xa5, 0x08, 0xd2, 0x6b, 0xe7, 0xde, 0xea, 0x42,
    }};
  return &hash;
}

#include <assert.h>
#include <string.h>

// Include directives for referenced types
#include "ros_robot_controller_msgs/msg/detail/pwm_servo_state__functions.h"

// Hashes for external referenced types
#ifndef NDEBUG
static const rosidl_type_hash_t ros_robot_controller_msgs__msg__PWMServoState__EXPECTED_HASH = {1, {
    0xbf, 0xa7, 0x78, 0x8b, 0x9c, 0x12, 0x6d, 0x14,
    0x99, 0x28, 0x0a, 0x76, 0x9d, 0x74, 0x9a, 0x75,
    0x7d, 0x40, 0x2c, 0xff, 0xf9, 0x2e, 0xa2, 0x17,
    0x1d, 0x46, 0xdb, 0x0e, 0xf1, 0x32, 0xba, 0x6d,
  }};
#endif

static char ros_robot_controller_msgs__msg__SetPWMServoState__TYPE_NAME[] = "ros_robot_controller_msgs/msg/SetPWMServoState";
static char ros_robot_controller_msgs__msg__PWMServoState__TYPE_NAME[] = "ros_robot_controller_msgs/msg/PWMServoState";

// Define type names, field names, and default values
static char ros_robot_controller_msgs__msg__SetPWMServoState__FIELD_NAME__state[] = "state";
static char ros_robot_controller_msgs__msg__SetPWMServoState__FIELD_NAME__duration[] = "duration";

static rosidl_runtime_c__type_description__Field ros_robot_controller_msgs__msg__SetPWMServoState__FIELDS[] = {
  {
    {ros_robot_controller_msgs__msg__SetPWMServoState__FIELD_NAME__state, 5, 5},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_NESTED_TYPE_UNBOUNDED_SEQUENCE,
      0,
      0,
      {ros_robot_controller_msgs__msg__PWMServoState__TYPE_NAME, 43, 43},
    },
    {NULL, 0, 0},
  },
  {
    {ros_robot_controller_msgs__msg__SetPWMServoState__FIELD_NAME__duration, 8, 8},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_DOUBLE,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
};

static rosidl_runtime_c__type_description__IndividualTypeDescription ros_robot_controller_msgs__msg__SetPWMServoState__REFERENCED_TYPE_DESCRIPTIONS[] = {
  {
    {ros_robot_controller_msgs__msg__PWMServoState__TYPE_NAME, 43, 43},
    {NULL, 0, 0},
  },
};

const rosidl_runtime_c__type_description__TypeDescription *
ros_robot_controller_msgs__msg__SetPWMServoState__get_type_description(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static bool constructed = false;
  static const rosidl_runtime_c__type_description__TypeDescription description = {
    {
      {ros_robot_controller_msgs__msg__SetPWMServoState__TYPE_NAME, 46, 46},
      {ros_robot_controller_msgs__msg__SetPWMServoState__FIELDS, 2, 2},
    },
    {ros_robot_controller_msgs__msg__SetPWMServoState__REFERENCED_TYPE_DESCRIPTIONS, 1, 1},
  };
  if (!constructed) {
    assert(0 == memcmp(&ros_robot_controller_msgs__msg__PWMServoState__EXPECTED_HASH, ros_robot_controller_msgs__msg__PWMServoState__get_type_hash(NULL), sizeof(rosidl_type_hash_t)));
    description.referenced_type_descriptions.data[0].fields = ros_robot_controller_msgs__msg__PWMServoState__get_type_description(NULL)->type_description.fields;
    constructed = true;
  }
  return &description;
}

static char toplevel_type_raw_source[] =
  "ros_robot_controller_msgs/PWMServoState[] state\n"
  "\n"
  "float64 duration";

static char msg_encoding[] = "msg";

// Define all individual source functions

const rosidl_runtime_c__type_description__TypeSource *
ros_robot_controller_msgs__msg__SetPWMServoState__get_individual_type_description_source(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static const rosidl_runtime_c__type_description__TypeSource source = {
    {ros_robot_controller_msgs__msg__SetPWMServoState__TYPE_NAME, 46, 46},
    {msg_encoding, 3, 3},
    {toplevel_type_raw_source, 66, 66},
  };
  return &source;
}

const rosidl_runtime_c__type_description__TypeSource__Sequence *
ros_robot_controller_msgs__msg__SetPWMServoState__get_type_description_sources(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_runtime_c__type_description__TypeSource sources[2];
  static const rosidl_runtime_c__type_description__TypeSource__Sequence source_sequence = {sources, 2, 2};
  static bool constructed = false;
  if (!constructed) {
    sources[0] = *ros_robot_controller_msgs__msg__SetPWMServoState__get_individual_type_description_source(NULL),
    sources[1] = *ros_robot_controller_msgs__msg__PWMServoState__get_individual_type_description_source(NULL);
    constructed = true;
  }
  return &source_sequence;
}
