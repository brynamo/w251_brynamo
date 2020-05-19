import paho.mqtt.client as mqtt
import cv2
import numpy as np
import datetime

#IBM COS Set Up
import ibm_boto3
from ibm_botocore.client import Config, ClientError


# Constants for IBM COS values
COS_ENDPOINT = "https://s3.wdc.us.cloud-object-storage.appdomain.cloud" # Current list avaiable at https://control.cloud-object-storage.cloud.ibm.com/v2/endpoints
COS_API_KEY_ID = "lu9XK6FLG2m3awTjRTwJz-FbqDpvq6ANuUzZZjqITYqO" # eg "W00YiRnLW4a3fTjMB-odB-2ySfTrFBIQQWanc--P3byk"
COS_AUTH_ENDPOINT = "https://iam.cloud.ibm.com/identity/token"
COS_RESOURCE_CRN = "crn:v1:bluemix:public:cloud-object-storage:global:a/e8a3fa73ecba48a7b4150f1ec2d94969:9eb3112c-707d-4d6e-bcad-56f6f28f3645::" # eg "crn:v1:bluemix:public:cloud-object-storage:g$

# Create resource
cos = ibm_boto3.resource("s3",
    ibm_api_key_id=COS_API_KEY_ID,
    ibm_service_instance_id=COS_RESOURCE_CRN,
    ibm_auth_endpoint=COS_AUTH_ENDPOINT,
    config=Config(signature_version="oauth"),
    endpoint_url=COS_ENDPOINT
)


def create_img_file(bucket_name, item_name, file):
    print("Creating new item: {0}".format(item_name))
    try:
        cos.Object(bucket_name, item_name).put(
            Body=file
        )
        print("Item: {0} created!".format(item_name))
    except ClientError as be:
        print("CLIENT ERROR: {0}\n".format(be))
    except Exception as e:
        print("Unable to create text file: {0}".format(e))



#MQTT Set up for local
LOCAL_MQTT_HOST = "172.17.0.2"
LOCAL_MQTT_PORT = 1883
LOCAL_MQTT_TOPIC = "face_detection/video_stream"
#MQTT Set up for remote
REMOTE_MQTT_HOST = "172.17.0.6"
REMOTE_MQTT_PORT = 1833
REMOTE_MQTT_TOPIC = "remote/video_stream"

#MQTT Helper Functions
def on_connect_local(client, userdata, flags, rc):
        print "connected to local broker with rc: " + str(rc)
        client.subscribe(REMOTE_MQTT_TOPIC)

def on_message(client, userdata, msg):
	try:
#		numpy_array = np.frombuffer(msg.payload)
#		sent_img = cv2.imdecode(numpy_array, 1)
		file_name = "sent_image"+ datetime.datetime.now().strftime("%m-%d-%Y_%H:%M:%S") + ".png"
#		file_name = "/home/brynamo/Documents/w251/bryan_working/images/sent_image"+ datetime.datetime.now().strftime("%m-%d-%Y_%H:%M:%S") + ".png"

#		cv2.imwrite(file_name, sent_img)
		create_img_file("hw3-output-images", file_name, msg.payload)
        except:
                print "Unexpected error: ", sys.exc_info()[0]

local_mqttclient = mqtt.Client()
local_mqttclient.on_connect = on_connect_local
local_mqttclient.connect(LOCAL_MQTT_HOST, LOCAL_MQTT_PORT, 60)
local_mqttclient.on_message = on_message

local_mqttclient.loop_forever()
