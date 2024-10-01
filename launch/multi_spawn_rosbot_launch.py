import os
from ament_index_python.packages import get_package_prefix
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, TextSubstitution
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

import xacro

def gen_robot_list(number_of_robots):

    robots = []

    for i in range(number_of_robots):
        robot_name = "rosbot_"+str(i+1)
        x_pos = float(i)
        robots.append({'name': robot_name, 'x_pose': x_pos, 'y_pose': 0.0, 'z_pose': 0.01})

    return robots 

def generate_launch_description():

    # Check if we're told to use sim time
    use_sim_time = LaunchConfiguration('use_sim_time', default='true')

    # Process the URDF file
    pkg_my_bot = os.path.join(get_package_share_directory('my_bot'))
    xacro_file = os.path.join(pkg_my_bot,'description','robot.urdf.xacro')
    #assert os.path.exists(xacro_file), "The box_bot.xacro doesnt exist in "+str(xacro_file)  


    # Names and poses of the robots
    robots = gen_robot_list(5)

    # Remapping is required for state publisher otherwise /tf and /tf_static 
    # will get be published on root '/' namespace
    remappings = [('/tf', 'tf'), ('/tf_static', 'tf_static')]
    arrNodes= []
      
    for robot in robots:

        namespace = [ '/' + robot['name']]

        robot_description_config = xacro.process_file(xacro_file, mapping={
            "namespace":namespace,
        },
        )
        
        robot_desc = robot_description_config.toxml()

        #Create rosbot_state_publisher nodes
        params ={'robot_description': robot_desc, 'use_sime_time': use_sim_time}
        rosbot_state_publisher = Node(
            package="robot_state_publisher",
            namespace=namespace,
            executable="robot_state_publisher",
            name="robot_state_publisher",
            output="screen",
            parameters=[params]
            #remappings=remappings
        )
        arrNodes.append(rosbot_state_publisher)

        #Spawn rosbot entities
        spawn_rosbot = Node(
            package="gazebo_ros",
            executable='spawn_entity.py', 
            namespace=namespace,
            arguments=[
                '-topic', 'robot_description',
                '-entity',robot['name'],
                '-robot_namespace', robot['name'],
                '-x', str(robot['x_pose']),
                '-y', str(robot['y_pose']),
                '-z', str(robot['z_pose'])],
            parameters=[{'use_sime_time': use_sim_time}],
            output='screen')
        arrNodes.append(spawn_rosbot)

        params = { 'use_sim_time': use_sim_time}
        joint_state_publisher_node = Node(
            package='joint_state_publisher',
            executable='joint_state_publisher',
            name='joint_state_publisher',
            namespace=namespace,
            parameters=[params]
            #remappings=remappings
            )
        arrNodes.append(joint_state_publisher_node)

    ld = LaunchDescription()
    
    for node in arrNodes:
        ld.add_action(node)
    
    return ld