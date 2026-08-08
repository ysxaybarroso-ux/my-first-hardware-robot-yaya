FROM ros:humble-ros-base 

RUN apt update && apt install -y ros-humble-navigation2 ros-humble-nav2-bringup ros-humble-slam-toolbox
