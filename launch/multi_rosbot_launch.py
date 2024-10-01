import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.actions import IncludeLaunchDescription
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():

    pkg_my_bot = get_package_share_directory('my_bot')

    # Sart World
    start_world = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_my_bot, 'launch', 'start_world_launch.py'),
        )
    )

    #spawn rosbot
    spawn_rosbot_world = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_my_bot, 'launch', 'multi_spawn_rosbot_launch.py'),
        )
    )     

    return LaunchDescription([
        start_world,
        spawn_rosbot_world
    ])