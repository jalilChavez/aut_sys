#!/usr/bin/python3
import rospy
import numpy as np
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
from pbot.msg import motor, distance

class controller():
    def __init__(self):
        self._cmd_pub = rospy.Publisher('/pbot_diff_drive_controller/cmd_vel', Twist, queue_size=1)
        rospy.Subscriber('/pbot/laser/scan', LaserScan, self.__lidarCallback, queue_size=1)
        # Initialize node pbot
        rospy.init_node('pbot', anonymous=True)
        self.rate = rospy.Rate(10)

    def __lidarCallback(self,data):
        print("[pbot] Received %d values"%(len(data.ranges)))
        print("[pbot] Average distance is %0.4f"%(self.get_avg_dist(data.ranges)))
        #print(data.ranges[0])
    
    def get_avg_dist(self,data):
        data = list(data)
        data = np.array(data)
        return np.mean(data[(data != float('Inf'))])
    
    def set_pbot_head_speed(self, head, speed):
        twist = Twist()
        twist.linear.x = speed
        twist.angular.z = head

    def run(self):
        
        while not rospy.is_shutdown():
            '''
                Code implementation goes here, if necesary you can create your
                own package annd call it from here.
            '''
            self.set_pbot_head_speed(head=0.0, speed=1.0)
            self._cmd_pub.publish(twist)
        self.rate.sleep()

if __name__ == '__main__':
    try:
        controller().run()
    except rospy.ROSInterruptException:
        pass

