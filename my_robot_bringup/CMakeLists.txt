cmake_minimum_required(VERSION 3.0.2)
project(my_robot_bringup)


## Find catkin macros and libraries
find_package(catkin REQUIRED COMPONENTS
  gmapping
  robot_state_publisher
  roscpp
  rospy
  tf
  nav_msgs
  std_msgs
  gazebo_msgs
)

###################################
## catkin specific configuration ##
###################################
catkin_package(
#  INCLUDE_DIRS include
#  LIBRARIES my_robot_bringup
#  CATKIN_DEPENDS gmapping robot_state_publisher roscpp
#  DEPENDS system_lib
)

###########
## Build ##
###########

## Specify additional locations of header files
## Your package locations should be listed before other locations
include_directories(
  include
  ${catkin_INCLUDE_DIRS}
)

# include_directories(
#   ${PROJECT_SOURCE_DIR}/src/my_robot/my_robot_bringup/include
# )


## Declare a C++ library
# add_library(${PROJECT_NAME}
#   src/${PROJECT_NAME}/my_robot_bringup.cpp
# )

## Add cmake target dependencies of the library
## as an example, code may need to be generated before libraries
## either from message generation or dynamic reconfigure
# add_dependencies(${PROJECT_NAME} ${${PROJECT_NAME}_EXPORTED_TARGETS} ${catkin_EXPORTED_TARGETS})

## Declare a C++ executable
add_executable(localization src/localization.cpp)
target_link_libraries(localization ${catkin_LIBRARIES})

# adding the odom publisher node
catkin_install_python(PROGRAMS
  scripts/odom_publisher.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)

#############
## Install ##
#############

