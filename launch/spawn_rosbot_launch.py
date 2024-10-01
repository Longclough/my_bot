import os
from ament_index_python.packages import get_package_prefix
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

import xacro


def generate_launch_description():

    # Check if we're told to use sim time
    use_sim_time = LaunchConfiguration('use_sim_time', default='true')

    # Process the URDF file
    pkg_my_bot = os.path.join(get_package_share_directory('my_bot'))

    xacro_file = os.path.join(pkg_my_bot,'description','robot.urdf.xacro')
    #assert os.path.exists(xacro_file), "The box_bot.xacro doesnt exist in "+str(xacro_file) 

 
    robot_description_config = xacro.process_file(xacro_file)
    robot_desc = robot_description_config.toxml()


    #Create a rosbot_state_publisher node
    params = {'robot_description':robot_desc, 'use_sime_time': use_sim_time}
    rosbot_state_publisher = Node(
            package="robot_state_publisher",
            executable="robot_state_publisher",
            name="robot_state_publisher",
            output="screen",
            parameters=[params])
  
    #Spawn rosbot entity
    spawn_rosbot = Node(package="gazebo_ros",
    executable='spawn_entity.py',
    arguments=['-topic', 'robot_description','-entity','my_bot'],
    output='screen')

    # Launch!
    return LaunchDescription([
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='false',
            description='Use simulation (Gazebo) clock if true'),
        rosbot_state_publisher,
        spawn_rosbot
    ])
