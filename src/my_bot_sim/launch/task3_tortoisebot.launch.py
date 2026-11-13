import os
from launch import LaunchDescription
from ament_index_python import get_package_share_directory
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

def generate_launch_description():
    pkg_name = "my_bot_sim"
    pkg = get_package_share_directory(pkg_name)
    urdf_file = os.path.join(pkg, 'urdf', 'ball.urdf')

    return LaunchDescription([
        IncludeLaunchDescription(PythonLaunchDescriptionSource([os.path.join(pkg,'launch', 'gazebo.launch.py' )])),
        
        Node(package=pkg_name,
             executable="finding_obstracle.py"),
        
        Node(package=pkg_name,
             executable="object_follow.py"),
        
        Node(package=pkg_name,
             executable="ball_move.py"),

        Node(package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=['-file', urdf_file, '-entity', 'my_ball', '-x', '5.0', '-y', '5.0', '-z', '0.0'],
        output = 'screen')
        
    ])