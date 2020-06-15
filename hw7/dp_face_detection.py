#Imports
import cv2
import numpy
import paho.mqtt.client as mqtt
from PIL import Image
import sys
import os
import urllib
import tensorflow.contrib.tensorrt as trt
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import tensorflow as tf
import numpy as np
import time
from tf_trt_models.detection import download_detection_model, build_detection_graph

# https://github.com/yeephycho/tensorflow-face-detection
FROZEN_GRAPH_NAME = 'data/frozen_inference_graph_face.pb'
!wget https://github.com/yeephycho/tensorflow-face-detection/blob/master/model/frozen_inference_graph_face.pb?raw=true -O {FROZEN_GRAPH_NAME}

output_dir=''
frozen_graph = tf.GraphDef()
with open(os.path.join(output_dir, FROZEN_GRAPH_NAME), 'rb') as f:
  frozen_graph.ParseFromString(f.read())


# https://github.com/NVIDIA-AI-IOT/tf_trt_models/blob/master/tf_trt_models/detection.py
INPUT_NAME='image_tensor'
BOXES_NAME='detection_boxes'
CLASSES_NAME='detection_classes'
SCORES_NAME='detection_scores'
MASKS_NAME='detection_masks'
NUM_DETECTIONS_NAME='num_detections'

input_names = [INPUT_NAME]
output_names = [BOXES_NAME, CLASSES_NAME, SCORES_NAME, NUM_DETECTIONS_NAME]

#Load Frozen Graph
trt_graph = trt.create_inference_graph(
    input_graph_def=frozen_graph,
    outputs=output_names,
    max_batch_size=1,
    max_workspace_size_bytes=1 << 25,
    precision_mode='FP16',
    minimum_segment_size=50
)

#Create Session and load Graph
tf_config = tf.ConfigProto()
tf_config.gpu_options.allow_growth = True

tf_sess = tf.Session(config=tf_config)

# use this if you want to try on the optimized TensorRT graph
# Note that this will take a while
# tf.import_graph_def(trt_graph, name='')

# use this if you want to try directly on the frozen TF graph
# this is much faster
tf.import_graph_def(frozen_graph, name='')

tf_input = tf_sess.graph.get_tensor_by_name(input_names[0] + ':0')
tf_scores = tf_sess.graph.get_tensor_by_name('detection_scores:0')
tf_boxes = tf_sess.graph.get_tensor_by_name('detection_boxes:0')
tf_classes = tf_sess.graph.get_tensor_by_name('detection_classes:0')
tf_num_detections = tf_sess.graph.get_tensor_by_name('num_detections:0')



#Env Set up
## capture set up
cap = cv2.VideoCapture(1)

#MQTT Set up
LOCAL_MQTT_HOST = "172.17.0.2"
LOCAL_MQTT_PORT = 1883
LOCAL_MQTT_TOPIC = "face_detection/video_stream"


#MQTT Helper Functions
def on_connect_local(client, userdata, flags, rc):
        print("connected to local broker with result code: " + str(rc))
        client.subscribe(LOCAL_MQTT_TOPIC)

def on_message(client, userdata, msg):
        try:
                print("Message Received! \n")
                print("Message Was: " + msg.payload)
        except:
                print("Unexpected error: ", sys.exc_info()[0])

local_mqttclient = mqtt.Client()
local_mqttclient.on_connect = on_connect_local
local_mqttclient.connect(LOCAL_MQTT_HOST, LOCAL_MQTT_PORT, 60)
local_mqttclient.on_message = on_message
local_mqttclient.loop_start()

#Set up frame capture
for j in range(15):
        #Read data from the camera
        ret, img = cap.read()

        image_resized = cv2.resize(img, (300, 300))
        image = np.array(img)
        
        scores, boxes, classes, num_detections = tf_sess.run([tf_scores, tf_boxes, tf_classes, tf_num_detections], feed_dict={
tf_input: image_resized[None, ...]
})

        boxes = boxes[0] # index by 0 to remove batch dimension
        scores = scores[0]
        classes = classes[0]
        num_detections = num_detections[0]
        
        DETECTION_THRESHOLD = 0.5


        # plot boxes exceeding score threshold
        for i in range(int(num_detections)):
            if scores[i] < DETECTION_THRESHOLD:
                continue
            # scale box to image coordinates
            box = boxes[i] * np.array([image.shape[0], image.shape[1], image.shape[0], image.shape[1]])
            
            int_box = np.rint(box).astype('int')
            
            #create a frame around the face
            frame = cv2.rectangle(image,(int_box[1], int_box[0]),(int_box[1] + (int_box[3] - int_box[1]),int_box[0] + (int_box[2] - int_box[0])),(255,0,0),2)
            cv2.imwrite('face_img' + str(j) + '.png', frame)
        #encode and package up image for message
        retval, cropped_img = cv2.imencode('.png', frame)
        msg = cropped_img.tobytes()
        local_mqttclient.publish(LOCAL_MQTT_TOPIC, payload=msg, qos=2, retain=False)
            
cap.release()
local_mqttclient.loop_stop()
cv2.destroyAllWindows()
