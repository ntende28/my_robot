#!/usr/bin/env python

# importing the necessary dependencies
import geometry_msgs
import rospy
import tf2_ros
from nav_msgs.msg import Odometry
from std_msgs.msg import Header
from gazebo_msgs.srv import GetModelState, GetModelStateRequest

def main():

    # creating our odom publisher node
    rospy.init_node("odom_publisher")
    
    # creating the publisher object with Odometry msg type, and queue - 10msgs
    odom_publisher = rospy.Publisher("/my_odom", Odometry, queue_size=10)
    # Create a TransformBroadcaster object
    tf_broadcaster = tf2_ros.TransformBroadcaster()
    # Creating a transform_broadcaster for map → base_link
    static_tf_broadcaster = tf2_ros.StaticTransformBroadcaster()  
    
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
    r = rospy.Rate(10)

    # Static transform (map → odom)
    static_transform = geometry_msgs.msg.TransformStamped()
    static_transform.header.stamp = rospy.Time.now()
    static_transform.header.frame_id = "map"
    static_transform.child_frame_id = "odom"
    static_transform.transform.translation.x = 0.0
    static_transform.transform.translation.y = 0.0
    static_transform.transform.translation.z = 0.0
    static_transform.transform.rotation.w = 1.0
    static_tf_broadcaster.sendTransform(static_transform)  # Publish once

    while not rospy.is_shutdown():
        try:
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
            
            # Create the transform message
            transform = geometry_msgs.msg.TransformStamped()
            transform.header.stamp = header.stamp
            transform.header.frame_id = "odom"  # Parent frame
            transform.child_frame_id = "base_link"  # Child frame
            
            # set translation from odom data 
            transform.transform.translation.x = result.pose.position.x
            transform.transform.translation.y = result.pose.position.y
            transform.transform.translation.z = result.pose.position.z
            
            # Set rotation from odometry data
            transform.transform.rotation = result.pose.orientation

            # Broadcast the transform
            tf_broadcaster.sendTransform(transform)

            # creating a time delay
            r.sleep()
        except:
            rospy.logwarn_once("Odom publisher node has been shutdown ...")

if __name__ == "__main__":
    main()