#!/usr/bin/env python

# importing the necessary dependencies
import rospy
from nav_msgs.msg import Odometry
from std_msgs.msg import Header
from gazebo_msgs.srv import GetModelState, GetModelStateRequest

def main():

    # creating our odom publisher node
    rospy.init_node("odom_publisher")

    # creting the publisher object with Odometry msg type, and queue - 10msgs
    odom_publisher = rospy.Publisher("/my_odom", Odometry, queue_size=10)

    # waiting for the service to start i.e. service -> gazebo/get_model_state
    rospy.wait_for_service("/gazebo/get_model_state")
    #creating a proxy to call the service of type GetModeState i.e. service -> gazebo/get_model_state
    get_model_srv = rospy.ServiceProxy("/gazebo/get_model_state", GetModelState)

    # creating the odom headers
    odom = Odometry()
    header = Header()
    header.frame_id = '/odom'

    # creating the model object
    model = GetModelStateRequest()
    model.model_name = 'my_robot_description'

    # publishing frequency
    r = rospy.Rate(3)

    while not rospy.is_shutdown():
        # get result returned from the model by calling the proxy service
        result = get_model_srv(model)

        # set the odom message
        odom.pose.pose = result.pose
        odom.twist.twist = result.twist

        # updating the message headers
        header.stamp = rospy.Time.now()
        odom.header = header

        # publishing our message using the publisher object
        odom_publisher.publish(odom)

        # creating a time delay
        r.sleep()
        # rospy.spin()

if __name__ == "__main__":
    main()