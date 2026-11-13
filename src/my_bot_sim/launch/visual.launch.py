import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    package_name = "my_bot_sim"
    pkg_dict = get_package_share_directory(package_name)
    urdf_file = os.path.join(pkg_dict, "urdf", "tortoise_bot.urdf")
    rviz_file = os.path.join(pkg_dict, "rviz", "config.rviz")

    with open(urdf_file,"r") as infp:
        robot_configuration = infp.read()

    node_robot_state_publisher = Node(
            package="robot_state_publisher",
            executable="robot_state_publisher",
            output='screen',
            parameters=[{'robot_description' : robot_configuration}]
        )

    node_rviz = Node(
        package="rviz2",
        executable="rviz2",
        arguments= ['-d', rviz_file],
        condition= None
    )
    return LaunchDescription([
        node_robot_state_publisher,
        node_rviz
    ])