#!/usr/bin/env python

import numpy as np
import cv2, cv_bridge
import rospy

from geometry_msgs.msg import Twist
from sensor_msgs.msg import Image
from std_srvs.srv import Empty



def enter_teleop(req):
    global last_press, state
    state = 'teleop'
    last_press = rospy.Time.now()
    return([])


def camera_callback(msg):

    image = bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')

    hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
    #dark_green = np.array([50,90,90])
    #bright_green = np.array([90,255,255])
    dark_yellow = np.array([50,50,170])
    bright_yellow = np.array([255,255,170])
    # Threshold the HSV image to get only greenish colors
    mask = cv2.inRange(hsv, dark_yellow, bright_yellow)

    # Mask the image by cropping appropriately
    (height, width, depth) = image.shape
    top_level = height / 2
    bottom_level = top_level + 80
    mask[0:top_level, 0:width] = 0
    mask[bottom_level:height, 0:width] = 0

    Moments = cv2.moments(mask)
    if Moments['m00'] > 0:
        centroid_x = int(Moments['m10'] / Moments['m00'])
        centroid_y = int(Moments['m01'] / Moments['m00'])
        #Create Predator like representation of where the focus is
        cv2.circle(image, (centroid_x-5, centroid_y+3), 3, (10,10,255), -1)
        cv2.circle(image, (centroid_x+5, centroid_y+3), 3, (10,10,255), -1)
        cv2.circle(image, (centroid_x, centroid_y-3), 3, (10,10,255), -1)

        # Use np.clip to have bounded values for Velocity
        msgout.linear.x = np.clip(msgout.linear.x + 0.05, linear_speed_lower_limit, linear_speed_upper_limit)
        msgout.angular.z = np.clip(0.01 * (width / 2 - centroid_x),-angular_speed_upper_limit, angular_speed_upper_limit)

    else:
        msgout.linear.x = np.clip(msgout.linear.x - 0.05, linear_speed_lower_limit, linear_speed_upper_limit)
        msgout.angular.z = np.clip(msgout.angular.z + 0.05, 0, angular_speed_upper_limit)

    # Publish if not stopped using Teleop
    if rospy.Time.now() - last_press > resume_delay:
        pub.publish(msgout)
    # If stopped using teleop
    else:
        msgout.linear.x = linear_speed_lower_limit
        msgout.angular.z = 0

    cv2.imshow("Line follower", image[:height,:,:])
    cv2.waitKey(2)


if __name__ == "__main__":

    # Global parameters
    resume_delay = rospy.Duration.from_sec(rospy.get_param("/resume_delay"))
    linear_speed_upper_limit = rospy.get_param("/max_speed")
    linear_speed_lower_limit = 0
    angular_speed_upper_limit = 0.8

    rospy.init_node('line_navigator', anonymous=True)
    bridge = cv_bridge.CvBridge()
    cv2.namedWindow("Line_follower", 1)
    
    rospy.sleep(1)
    last_press = rospy.Time.now() - resume_delay
    s = rospy.Service('button_press', Empty, enter_teleop)

    pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)
    sub = rospy.Subscriber('/right/image_raw', Image, camera_callback)
    msgout = Twist()

    rospy.spin()
