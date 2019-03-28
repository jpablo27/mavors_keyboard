#!/usr/bin/env python

import rospy
import tf
import math
from std_msgs.msg import String
from geometry_msgs.msg import TwistStamped, Twist, PoseStamped
from keyboard.msg import Key

cmd = TwistStamped()
orientation = 0.0

FB=0.0
LR=0.0

def control():
	rospy.Subscriber("/keyboard/keydown",Key,down)
	rospy.Subscriber("/keyboard/keyup",Key,up)
	rospy.Subscriber("/mavros/local_position/pose",PoseStamped,pose)
	pub = rospy.Publisher('/mavros/setpoint_velocity/cmd_vel',TwistStamped, queue_size = 10)
	rospy.init_node('control', anonymous=True)
	rate = rospy.Rate(10) # 10hz
	while not rospy.is_shutdown():
		#rospy.loginfo(cmd)
		pub.publish(cmd)
		rate.sleep()

def down(data):

	global orientation, FB, LR, cmd

	if(chr(data.code) == 'w'):
		FB= 0.5
	if(chr(data.code) == 'a'):
		LR= -0.5
	if(chr(data.code) == 's'):
		FB= -0.5
	if(chr(data.code) == 'd'):
		LR=0.5

	cmd.twist.linear.x= FB*math.cos(orientation)+LR*math.sin(orientation)
	cmd.twist.linear.y= FB*math.sin(orientation)-LR*math.cos(orientation)
	
	if(chr(data.code) == 'q'):
		cmd.twist.angular.z=0.2
	if(chr(data.code) == 'e'):
		cmd.twist.angular.z=-0.2


def up(data):
	global FB, LR, cmd, orientation
	if(chr(data.code) == 'w'):
		FB=0
	if(chr(data.code) == 'a'):
		LR=0
	if(chr(data.code) == 's'):
		FB=0
	if(chr(data.code) == 'd'):
		LR=0

	cmd.twist.linear.x= FB*math.cos(orientation)+LR*math.sin(orientation)
	cmd.twist.linear.y= FB*math.sin(orientation)+LR*math.cos(orientation)

	if(chr(data.code) == 'q'):
		cmd.twist.angular.z=0
	if(chr(data.code) == 'e'):
		cmd.twist.angular.z=0

def pose(data):
	global orientation
	qw = data.pose.orientation.w
	qx = data.pose.orientation.x
	qy = data.pose.orientation.y
	qz = data.pose.orientation.z
	(r,p,y) = tf.transformations.euler_from_quaternion([qx,qy,qz,qw])
	orientation = math.atan2(math.sin(y),math.cos(y))
	



if __name__ == '__main__':
	try:
		control()
	except rospy.ROSInterruptException:
		pass