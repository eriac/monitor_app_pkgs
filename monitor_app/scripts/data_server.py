#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from opencv_apps.msg import FaceArrayStamped
from geometry_msgs.msg import PointStamped
from monitor_msgs.msg import MongoData, MongoDataList
from monitor_msgs.srv import RequestMongoData, RequestMongoDataResponse
from mongodb_store.message_store import MessageStoreProxy

class Server:
    def __init__(self):
        rospy.Service('request_mongo', RequestMongoData, self.callback)
        self.msg_store = MessageStoreProxy(database="srs", collection="face_detect")

    def callback(self, msg):
        print("request")
        mongo_list = self.msg_store.query(MongoData._type)
        output = MongoDataList()
        try:
            for item in mongo_list:
                output.list.append(item[0])
        except rospy.ServiceException, e:
            print "Service call failed: %s"%e
        
        return RequestMongoDataResponse(output)

if __name__ == '__main__':
    rospy.init_node('server')
    server = Server()
    rospy.spin()
