#!/usr/bin/env python3
# license removed for brevity
from std_msgs.msg import String
import rospy
import subprocess
import time



def talker():
    pub = rospy.Publisher('chatter', String, queue_size=20)
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(10) # 10hz


    time.sleep(0.1)
    i=0
    while i<10: 
        hello_str = "hello world %s" % rospy.get_time()
        pub.publish(hello_str)

        print(hello_str)
        #rospy.loginfo(hello_str)
        time.sleep(0.1)
        
        i+=1
    
if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
