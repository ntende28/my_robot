cmake_minimum_required(VERSION 3.0.2)
project(my_robot_gazebo)

## Compile as C++11, supported in ROS Kinetic and newer
# add_compile_options(-std=c++11)

## Find catkin macros and libraries
find_package(catkin REQUIRED)

catkin_package()

include_directories(
# include
    ${catkin_INCLUDE_DIRS}
)


# install(DIRECTORY config launch
#   DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION})

