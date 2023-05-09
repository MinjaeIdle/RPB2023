from sensor_msgs.msg import Image, CompressedImage
from cv_bridge import CvBridge, CvBridgeError
from std_msgs.msg import Header
import rospy
import cv2


class DetermineColor:
    def __init__(self):
        self.image_sub = rospy.Subscriber('/camera/color/image_raw', Image, self.callback)
        self.color_pub = rospy.Publisher('/rotate_cmd', Header, queue_size=10)
        self.bridge = CvBridge()
        self.count = 0

    def callback(self, data):
        try:
            # listen image topic
            image = self.bridge.imgmsg_to_cv2(data, 'bgr8')

            # prepare rotate_cmd msg
            # DO NOT DELETE THE BELOW THREE LINES!
            msg = Header()
            msg = data.header
            msg.frame_id = '0'  # default: STOP
            
            
            cv2.imshow('Image', image)
            cv2.waitKey(1)
            

            # determine background color
            # TODO
            # determine the color and assing +1, 0, or, -1 for frame_id
            # msg.frame_id = '+1' # CCW (Blue background)
            # msg.frame_id = '0'  # STOP
            # msg.frame_id = '-1' # CW (Red background)
            image = cv2.resize(image, (50, 30))
            b, g, r = cv2.split(image)
            rows, columns = b.shape
            c_red, c_blue, c_green, c_yellow, c_magenta, c_cyan, c_white = 0, 0, 0, 0, 0, 0, 0
            for i in range(rows):
                for j in range(columns):
                    if b[i][j] > 150 and g[i][j] < 150 and r[i][j] < 150:
                        c_blue += 1
                    elif b[i][j] < 150 and g[i][j] < 150 and r[i][j] > 150:
                        c_red += 1
                    elif b[i][j] < 150 and g[i][j] > 150 and r[i][j] < 150:
                        c_green += 1
                    elif b[i][j] > 150 and g[i][j] > 150 and r[i][j] > 150:
                        c_white += 1
                    elif b[i][j] < 150 and g[i][j] > 150 and r[i][j] > 150:
                        c_yellow += 1
                    elif b[i][j] > 150 and g[i][j] < 150 and r[i][j] > 150:
                        c_magenta += 1
                    elif b[i][j] > 150 and g[i][j] > 150 and r[i][j] < 150:
                        c_cyan += 1
            c_blue = c_blue + c_cyan
            clist = [c_red, c_blue, c_green, c_yellow, c_magenta,c_white]
            if max(clist)==c_blue:
                msg.frame_id = '+1'
            elif max(clist)==c_red:
                msg.frame_id = '-1'
            else:
                msg.frame_id = '0'

            # publish color_state
            self.color_pub.publish(msg)

        except CvBridgeError as e:
            print(e)


    def rospy_shutdown(self, signal, frame):
        rospy.signal_shutdown("shut down")
        sys.exit(0)

if __name__ == '__main__':
    detector = DetermineColor()
    rospy.init_node('CompressedImages1', anonymous=False)
    rospy.spin()
