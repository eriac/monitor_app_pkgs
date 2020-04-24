#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from std_srvs.srv import Empty
from sensor_msgs.msg import Image
from opencv_apps.msg import FaceArrayStamped
from geometry_msgs.msg import PointStamped
from monitor_msgs.msg import MongoData
from mongodb_store.message_store import MessageStoreProxy
from cv_bridge import CvBridge, CvBridgeError
import base64
import cv2

class Listener:
    def __init__(self):
        rospy.Subscriber("/face_detection/faces", FaceArrayStamped, self.faceCallback)
        rospy.Subscriber("/image_raw_throttle", Image, self.imageCallback)
        self.bridge = CvBridge()
        self.last_base64 = None

        self.active=False
        self.counter=0
        self.threshold=2
        self.msg_store = MessageStoreProxy(database="srs", collection="face_detect")
        
    def faceCallback(self, msg):
        if self.active:
            if len(msg.faces) == 0:
                self.active = False
                print("inactivating")
        else:
            if len(msg.faces) > 0:
                if len(msg.faces[0].eyes) >= 2:
                    self.active= True
                    print("activating")
                    self.activating(msg)

    def imageCallback(self, msg):
        frame = self.bridge.imgmsg_to_cv2(msg, "bgr8")
        height = frame.shape[0]
        width = frame.shape[1]
        frame2 = cv2.resize(frame , (int(width*0.25), int(height*0.25)))
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 50]
        result, frame3 = cv2.imencode(".jpg", frame2, encode_param)
        self.last_base64 = base64.b64encode(frame3)

    def activating(self, msg):
        try:
            data = MongoData()
            data.stamp = rospy.get_rostime()
            data.x = msg.faces[0].face.x
            data.y = msg.faces[0].face.y
            data.image = self.last_base64
            p_id = self.msg_store.insert(data)            
        except rospy.ServiceException, e:
            print "Service call failed: %s"%e

if __name__ == '__main__':
    rospy.init_node('listener')
    listener = Listener()
    rospy.spin()
