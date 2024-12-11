import launch
import launch_ros
from ament_index_python.packages import get_package_share_directory
import launch_ros.parameter_descriptions


def generate_launch_description():

	# 获取默认路径
	urdf_tutorial_path = get_package_share_directory('fishbot_description')
	default_model_path = urdf_tutorial_path + '/urdf/first_robot.urdf'

	# 为launch声明参数
	action_declare_arg_model_path = launch.actions.DeclareLaunchArgument(
		name='model', default_value=default_model_path, description='urdf文件的绝对路径'
	)

	# 获取文件内容生成新的参数
	robot_description = launch_ros.parameter_descriptions.ParameterValue(
		launch.substitutions.Command(
			['xacro ', launch.substitutions.LaunchConfiguration('model')],
		),
		value_type=str
	)

	# 机器人状态发布节点
	robot_state_publisher_node = launch_ros.actions.Node(
		package='robot_state_publisher',
		executable='robot_state_publisher',
		parameters=[{'robot_description': robot_description}]
	)

	# 关节状态发布节点
	joint_state_publisher_node = launch_ros.actions.Node(
		package='joint_state_publisher',
		executable='joint_state_publisher'
	)

	default_rviz_config_path = urdf_tutorial_path + '/config/display_model.rviz'

	# Rviz节点
	rviz_node = launch_ros.actions.Node(
		package='rviz2',
		executable='rviz2',
		arguments=['-d', default_rviz_config_path]  # parameters是传递给ROS节点的参数，argument是命令行需要的参数
	)

	return launch.LaunchDescription(
		[
			action_declare_arg_model_path,
			robot_state_publisher_node,
			joint_state_publisher_node,
			rviz_node
		]
	)
