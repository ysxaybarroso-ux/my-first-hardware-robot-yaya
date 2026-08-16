from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.actions import ExecuteProcess
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    return LaunchDescription([
        ExecuteProcess(cmd=["python3", "/home/radxa/my-first-hardware-robot-yaya/code/perception/lidar_ros_node.py"]),
        ExecuteProcess(cmd=["python3",  "/home/radxa/my-first-hardware-robot-yaya/code/perception/odom_ros_node.py"]),
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(get_package_share_directory('slam_toolbox'), 'launch', 'online_async_launch.py')
            )
        ),
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(get_package_share_directory('nav2_bringup'), 'launch', 'navigation_launch.py')
            )
        ),
        ExecuteProcess(cmd=["python3",  "/home/radxa/my-first-hardware-robot-yaya/code/behavior/navigation_web.py"]),
        ExecuteProcess(cmd=["python3",  "/home/radxa/my-first-hardware-robot-yaya/code/behavior/cmd_vel_bridge.py"]),
    ])