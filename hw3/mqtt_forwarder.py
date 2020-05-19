import paho.mqtt.client as mqtt

#MQTT Set up for local
LOCAL_MQTT_HOST = "172.17.0.2"
LOCAL_MQTT_PORT = 1883
LOCAL_MQTT_TOPIC = "face_detection/video_stream"

REMOTE_MQTT_HOST = "172.17.0.6"
REMOTE_MQTT_PORT = 1833
REMOTE_MQTT_TOPIC = "remote/video_stream"

#MQTT Helper Functions
def on_connect_local(client, userdata, flags, rc):
        print "connected to local broker with rc: " + str(rc)
        client.subscribe(LOCAL_MQTT_TOPIC)

def on_message(client, userdata, msg):
        try:
                print "Message Received! \n"
                print "Message Was: " + msg.payload
		local_mqttclient.publish(REMOTE_MQTT_TOPIC, payload=msg.payload, qos=2, retain=False)
        except:
                print "Unexpected error: ", sys.exc_info()[0]

local_mqttclient = mqtt.Client()
local_mqttclient.on_connect = on_connect_local
local_mqttclient.connect(LOCAL_MQTT_HOST, LOCAL_MQTT_PORT, 60)
local_mqttclient.on_message = on_message

local_mqttclient.loop_forever()
