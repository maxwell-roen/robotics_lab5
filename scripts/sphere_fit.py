#!/usr/bin/env python3

import rospy
import numpy as np
from geometry_msgs.msg import Point
from robot_vision_lectures.msg import XYZarray
from robot_vision_lectures.msg import SphereParams
from math import sqrt


pts = []
pts_received = False
sphere_params_msg = SphereParams()



def get_pts(pts_in):
	global pts
	global pts_received
	pts = pts_in
	pts_received = True


# okay so I have my points. need to map these to BAP and solve for P, I think? (then get r out)
def fit_sphere():
	global pts
	global sphere_params_msg
	B = []
	A = []
	just_pts = pts.points
	num_pts = len(just_pts)
	# extract the coordinates to form A and B
	for i in range(num_pts):
		x = just_pts[i].x
		y = just_pts[i].y
		z = just_pts[i].z
		B.append([x ** 2 + y ** 2 + z ** 2])
		A.append([2 * x, 2 * y, 2 * z, 1])
	# which we can use to solve for P
	P = np.linalg.lstsq(A, B, rcond=None)[0]
	xc = P[0]
	yc = P[1]
	zc = P[2]
	r = sqrt(P[3] + xc ** 2 + yc ** 2 + zc ** 2)
	# store the results in a SphereParams msg that we can publish
	sphere_params_msg.xc = xc
	sphere_params_msg.yc = yc
	sphere_params_msg.zc = zc
	sphere_params_msg.radius = r
	return sphere_params_msg



if __name__ == '__main__':
	# define node
	rospy.init_node('sphere_fit', anonymous=True)
	# subscribe to /xyz_cropped_ball to get pts
	pts_sub = rospy.Subscriber('/xyz_cropped_ball', XYZarray, get_pts)
	# define the publisher to publish the sphere params
	pts_pub = rospy.Publisher('/sphere_params', SphereParams, queue_size = 1)
	# set freq loop
	rate = rospy.Rate(10)
	
	while not rospy.is_shutdown():
		if pts_received:
			result = fit_sphere()
			pts_pub.publish(result)
		rate.sleep()
	
