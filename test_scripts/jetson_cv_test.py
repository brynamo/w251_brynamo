#Imports
import cv2
import numpy
import paho.mqtt.client as mqtt

#Env Set up
## capture set up
cap = cv2.VideoCapture(0)

#Cascade Set up
face_cascade = cv2.CascadeClassifier('/usr/share/opencv4/haarcascades/haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('/usr/share/opencv4/haarcascades/haarcascade_eye.xml')

#MQTT Set up
LOCAL_MQTT_HOST = "172.17.0.2"
LOCAL_MQTT_PORT = 1883
LOCAL_MQTT_TOPIC = "test/first"

#MQTT Helper Functions
def on_connect_local(client, userdata, flags, rc):
	print "connected to local broker with result code: " + str(rc)
	client.subscribe(LOCAL_MQTT_TOPIC)

def on_message(client, userdata, msg):
	try:
		print "Message Received! \n"
		print "Message Was: " + msg.payload
	except:
		print "Unexpected error: ", sys.exc_info()[0]

local_mqttclient = mqtt.Client()
local_mqttclient.on_connect = on_connect_local
local_mqttclient.connect(LOCAL_MQTT_HOST, LOCAL_MQTT_PORT, 60)
#local_mqttclient.on_message = on_message
local_mqttclient.loop_start()

#Set up frame capture
while(True):
	#Read data from the camera
	ret, img = cap.read()
	#Convert to grayscale
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

	#Detect Faces
	faces = face_cascade.detectMultiScale(gray, 1.1, 4)
	for (x,y,w,h) in faces:
		#create a frame around the face
		frame = cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
		#set up coordinates for face in grey and color
		roi_gray = gray[y:y+h, x:x+w]
		roi_color = frame[y:y+h, x:x+w]
		#save image to local
		cv2.imwrite('face_img.png', roi_color)
		#encode and package up image for message
		retval, cropped_img = cv2.imencode('.png', img)
		msg = cropped_img.tobytes()
		local_mqttclient.publish("test/first", payload=msg, qos=2, retain=False)
		#show encoded images
		testerson = cv2.imdecode(cropped_img, 1)
	        cv2.imshow('cropped_img', testerson)


		#extra flare, set up rectangles for eyes
		eyes = eye_cascade.detectMultiScale(roi_gray)
		for (ex,ey,ew,eh) in eyes:
			cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)

	#Show the frame
#	testerson = cv2.imdecode('.png', cropped_img)
#	cv2.imshow('Video', testerson)
	
	#Set up kill
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

cap.release()
local_mqttclient.loop_stop()
cv2.destroyAllWindows()
