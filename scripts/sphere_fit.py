#!/usr/bin/env python3

import rospy
import numpy as np
from geometry_msgs.msg import Point # XYZarray is an array of these points
from robot_vision_lectures.msg import XYZarray # not sure why this can't find them in this packages msg dir, use this for now...
from robot_vision_lectures.msg import SphereParams # not sure if we need this yet, just bring it in for now.

pts = []
pts_received = False

def get_pts(pts_in):
	global pts
	global pts_received
	# just see if structure is working.
	print(f'from the callback, pts: {pts}')
	pts = pts_in
	pts_received = True


# okay so I have the pts, need to do the math...
def fit_sphere():




if __name__ == '__main__':
	# define node
	rospy.init_node('sphere_fit', anonymous=True)
	# subscribe to /xyz_cropped_ball to get pts
	pts_sub = rospy.Subscriber('/xyz_cropped_ball', XYZarray, get_pts)
	# define a publisher to...publish the pt cloud? not sure, not doing this yet.
	pts_pub = rospy.Publisher('/sphere_params', SphereParams, queue_size = 1)
	# set freq loop
	rate = rospy.Rate(10)
	
	# for now do nothing, just see if subscriber callback/general structure is working.
	while not rospy.is_shutdown():
		if pts_received:
			result = fit_sphere()
			pts_pub.publish(result)
		rate.sleep()
	
