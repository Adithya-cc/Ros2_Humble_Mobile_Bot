import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, TimerAction
from launch_ros.actions import Node
from launch.launch_description_sources import PythonLaunchDescriptionSource

def generate_launch_description():
    pkg_name = 'my_bot_sim'
    pkg_share = get_package_share_directory(pkg_name)

    # Paths
    urdf_file = os.path.join(pkg_share, 'urdf', 'tortoise_bot.urdf')
    world_path = os.path.join(pkg_share, 'worlds', 'custom_obstacle_world.world')

    # Read URDF
    with open(urdf_file, 'r') as infp:
        robot_desc = infp.read()

    # Robot State Publisher
    node_robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[{'robot_description': robot_desc}]
    )

    # Launch Gazebo with your custom world
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [os.path.join(get_package_share_directory('gazebo_ros'), 'launch', "gazebo.launch.py")]
        ),
        #launch_arguments=[('world', world_path)]
    )

    # Spawn robot after 5 seconds to ensure Gazebo is ready
    spawn_entry = TimerAction(
        period=5.0,
        actions=[Node(
            package='gazebo_ros',
            executable='spawn_entity.py',
            arguments=[
                '-topic', 'robot_description',
                '-entity', 'tortoise_bot',
                '-x', '0.0',
                '-y', '0.0',
                '-z', '0.15'
            ],
            output='screen'
        )]
    )

    # Launch description
    return LaunchDescription([
        node_robot_state_publisher,
        gazebo,
        spawn_entry
    ])
