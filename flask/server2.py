from flask import Flask, render_template
import paho.mqtt.client as mqtt  
import time 

app=Flask(__name__)
#mqtt_broker = "203.252.106.154"
mqtt_user = "iot"
mqtt_pwd = ".csee"
mqtt_broker = "192.168.2.4"

###########URL##################
pub_topic="iot/" + mqtt_broker
urlLed = "iot/" + mqtt_broker + "/led"
urlLedon = "iot/" + mqtt_broker + "/ledon"
urlLedoff = "iot/" + mqtt_broker + "/ledoff"
urlUsbled = "iot/" + mqtt_broker + "/usbled"
urlUsbledon = "iot/" + mqtt_broker + "/usbledon"
urlUsbledoff = "iot/" + mqtt_broker + "/usbledoff"
urlDht22 = "iot/" + mqtt_broker + "/dht22"
urlDht22_t = "iot/" + mqtt_broker + "/dht22_t"
urlDht22_h = "iot/" + mqtt_broker + "/dht22_h"
urlCds = "iot/" + mqtt_broker + "/cds"
urlPir  = "iot/" + "21400670" + "/pir"

subDht22 = "iot/" + mqtt_broker + "/dht22"
subDht22_t = "iot/" + mqtt_broker + "/dht22_t"
subDht22_h = "iot/" + mqtt_broker + "/dht22_h"
subCds = "iot/" + mqtt_broker + "/cds"
subPir = "iot/" + mqtt_broker + "/pir"

message='none'
#############option###############
temperatureValue = "none" 
humidityValue = "none" 
pirValue = "Not detected"
cdsValue = "none"
################### main ######################
@app.route('/')
def home():
        return home()
################## led ########################
@app.route('/'+urlLed)
def led():
	mqttc.publish(pub_topic,"light/led")
	return home()
@app.route('/'+urlLedon)
def ledon():
	mqttc.publish(pub_topic,"light/ledon")
	return home()
@app.route('/'+urlLedoff)
def ledoff():
	mqttc.publish(pub_topic,"light/ledoff")
	return home()
################## USBLED #####################
@app.route('/'+urlUsbled)
def usbled():
	mqttc.publish(pub_topic,"light/usbled")
	return home()
@app.route('/'+urlUsbledon)
def usbledon():
	mqttc.publish(pub_topic, "light/usbledon")
	return home()
@app.route('/'+urlUsbledoff)
def usbledoff():
	mqttc.publish(pub_topic, "light/usbledoff")
	return home()

################### dht22  ################## 
@app.route('/'+urlDht22)
def getDht22():
#	mqttc.publish(pub_topic, "sensor/dht22")	
	#time.sleep(0.2)
	mqttc.subscribe(subDht22)
	mqttc.subscribe(commonSubDht22)
@app.route('/'+urlDht22_t)
def getDht22_t():
	#mqttc.publish(pub_topic, "sensor/dht22_t")
	mqttc.subscribe(subDht22_t)
	mqttc.subscribe(commonSubDht22_t)
@app.route('/'+urlDht22_h)
def getDht22_h():
#	mqttc.publish(pub_topic, "sensor/dht22_h")
	mqttc.subscribe(subDht22_h)
################### cds  ######################
@app.route('/'+urlCds)
def getCds():
#	mqttc.publish(pub_topic, "sensor/cds")
	mqttc.subscribe(subCds)
@app.route('/'+urlPir)
def getPir():
	mqttc.subscribe(subPir)

################### Function defition #################
def on_message(mqttc, userdata, msg):
	global topic
	global message
	global temperatureValue
	global humidityValue
	global pirValue
	global cdsValue
	global ledValue
	global usbledValue
###	print(msg.topic+" "+str(msg.payload))
	topic = msg.topic
	message=str(msg.payload)
	print( str(message)+"message")
	print(topic)
	if topic == subDht22:
		dht22Value = message
	elif topic == subDht22_t:
		dht22_tIndex =message
	elif topic == subDht22_h:
		dht22_hIndex = message
	elif topic == subCds:
		cdsIndex = message
	elif topic == subPir:
		pirIndex = message
###	print ("Topic: " + topic + " msg: " + message)
def on_connection(mqttc, userdata, flags, rc):
	print("###Connected with result code " + str(rc))
	return home()	
if __name__=="__main__":
	mqttc = mqtt.Client("rpi3_1") 
	mqttc.username_pw_set(mqtt_user, mqtt_pwd) 
	mqttc.on_message=on_message 
	mqttc.on_connection=on_connection 
	mqttc.connect(mqtt_broker, 1883, 60) 
	mqttc.loop_start()
	app.run(host="0.0.0.0", port=80, debug=True) 
