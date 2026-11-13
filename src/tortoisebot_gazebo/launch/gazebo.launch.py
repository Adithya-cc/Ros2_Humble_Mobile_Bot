import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node

def generate_launch_description():
    package_name = 'tortoisebot_gazebo'
    
    # Path to your URDF
    urdf_file = os.path.join(get_package_share_directory(package_name), 'urdf', 'robot.urdf')
    world_path = os.path.join(get_package_share_directory(package_name), 'world', 'empty_world.world')

    with open(urdf_file, 'r') as infp:
        robot_desc = infp.read()

    # Path to the standard Gazebo World launch
    pkg_gazebo_ros = get_package_share_directory('gazebo_ros')
    gazebo_launch = os.path.join(pkg_gazebo_ros, 'launch', 'gazebo.launch.py')

    return LaunchDescription([
        # 1. Start Gazebo Server and Client
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(gazebo_launch),
            launch_arguments={'world': world_path}.items()
        ),

        # 2. Robot State Publisher (publishes the URDF to /robot_description)
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            output='screen',
            parameters=[{'robot_description': robot_desc, 'use_sim_time': True}]
        ),

        # 3. Spawn Entity (THIS IS THE FIXED PART)
        Node(
            package='gazebo_ros',
            executable='spawn_entity.py',
            arguments=['-topic', 'robot_description', '-entity', 'tortoisebot'],
            output='screen',
        )
    ])