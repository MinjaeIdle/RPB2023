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
            b, g, r = cv2.split(img)
            bgr = np.stack([b, g, r], axis=-1)
            colors = np.array([
                [0, 0, 255],  # Red
                [255, 0, 0],  # Blue
                [0, 255, 0],  # Green
                [0, 255, 255],  # Yellow
                [255, 0, 255],  # Magenta
                [255, 255, 255],  # White
            ])
            diff = np.abs(bgr[:, :, None] - colors[None, None])
            distances = np.linalg.norm(diff, axis=-1)
            color_counts = np.sum(distances < 150, axis=(0, 1))
            #print(color_counts)
            if max(color_counts)==color_counts[1]:
                msg.frame_id = '+1'  # Blue
            elif max(color_counts)==color_counts[0]:
                msg.frame_id = '-1'  # Red
            else:
                msg.frame_id = '0'  # etc
                
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
