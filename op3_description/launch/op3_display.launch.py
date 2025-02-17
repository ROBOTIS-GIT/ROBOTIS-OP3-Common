from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution, Command
from launch_ros.substitutions import FindPackageShare
from launch_ros.actions import Node

from launch_ros.parameter_descriptions import ParameterValue

def generate_launch_description():
  ld = LaunchDescription()

  op3_description_path = FindPackageShare('op3_description')
  op3_urdf_path = PathJoinSubstitution([op3_description_path, 'urdf', 'robotis_op3.urdf.xacro'])
  op3_description_content = ParameterValue(Command(['xacro ', op3_urdf_path]), value_type=str)

  default_rviz_config_path = PathJoinSubstitution([op3_description_path, 'rviz', 'op3.rviz'])

  # Launch description 
  # joint_state_publisher 
#   ld.add_action(Node(
#     package='joint_state_publisher',
#     executable='joint_state_publisher',
#     parameters=[{'source_list': ['/robotis/present_joint_states']}],
#     remappings=[('/joint_states', '/robotis/present_joint_states')])
#   )

  # joint_state_publisher_gui
  ld.add_action(Node(
    package='joint_state_publisher_gui',
    executable='joint_state_publisher_gui',
    parameters=[{'source_list': ['/robotis/present_joint_states']}],
    remappings=[('/joint_states', '/robotis/present_joint_states')])
  )

  # robot_state_publisher 
  ld.add_action(Node(
    package='robot_state_publisher',
    executable='robot_state_publisher',
    parameters=[{'robot_description': op3_description_content,}],
    remappings=[('/joint_states', '/robotis/present_joint_states'),],)
  )

  # Rviz 
  ld.add_action(Node(
    package='rviz2',
    executable='rviz2',
    name='rviz2',
    output='screen',
    arguments=['-d', default_rviz_config_path],)
  )

  return ld
