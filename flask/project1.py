from flask import Flask, render_template
import paho.mqtt.client as mqtt  
import time 

app=Flask(__name__)
mqtt_broker = "192.168.2.4"
mqtt_user = "iot"
mqtt_pwd = ".csee"

###########URL##################
pub_topic="iot/21400670"
urlLed = "iot/21400670/led"
urlLedon = "iot/21400670/ledon"
urlLedoff = "iot/21400670/ledoff"
urlUsbled = "iot/21400670/usbled"
urlUsbledon = "iot/21400670/usbledon"
urlUsbledoff = "iot/21400670/usbledoff"
urlDht22 = "iot/21400670/dht22"
urlDht22_t = "iot/21400670/dht22_t"
urlDht22_h = "iot/21400670/dht22_h"
urlCds = "iot/21400670/cds"
urlPir = "iot/21400670/pir"

subDht22 = "iot/21400670/sensor/dht22"
subDht22_t = "iot/21400670/sensor/dht22_t"
subDht22_h = "iot/21400670/sensor/dht22_h"
subCds = "iot/21400670/sensor/cds"
subPir = "iot/21400670/sensor/pir"

commonSubDht22 = "iot/ece30003/sensor/dht22"
commonSubDht22_t ="iot/ece30003/sensor/dht22_t"
commonSubDht22_h = "iot/ece30003/sensor/dht22_h"
commonSubCds = "iot/ece30003/sensor/cds"
commonSubPir = "iot/ece30003/senor/pir"

subLed = "iot/21400670/check/led"
subUsbled = "iot/21400670/check/usbled"
message='none'
#############option###############
ledBool = False 
ledValue = "Off"
temperatureValue = "none" 
humidityValue = "none" 
usbledValue = "Off"
usbledBool = False
pirValue = "Not detected"
pirBool = False
cdsValue = "none"
homeBool = True 
################### main ######################
@app.route('/')
def home():
	global homeBool
	global pirValue
	global ledValue
	global usbledValue
	if homeBool:
		homeBool = False
		getDht22()
		time.sleep(0.1)
		getCds()
		time.sleep(0.1)
	mqttc.loop_start()
	mqttc.subscribe(subPir)
	return render_template('index.html', temperature=temperatureValue, humidity=humidityValue, cds=cdsValue, pir=pirValue)

################## led ########################
@app.route('/'+urlLed)
def led():
	global ledBool
	global ledValue
	mqttc.publish(pub_topic,"light/led")
	return home()

@app.route('/'+urlLedon)
def ledon():
	global ledValue
	mqttc.publish(pub_topic,"light/ledon")
	return home()

@app.route('/'+urlLedoff)
def ledoff():
	global ledValue
	mqttc.publish(pub_topic,"light/ledoff")
	return home()

################## USBLED #####################
@app.route('/'+urlUsbled)
def usbled():
	global usbledBool
	global usbledValue
	mqttc.publish(pub_topic,"light/usbled")
	return home()

@app.route('/'+urlUsbledon)
def usbledon():
	global usbledValue
	mqttc.publish(pub_topic, "light/usbledon")
	return home()

@app.route('/'+urlUsbledoff)
def usbledoff():
	global usbledValue
	mqttc.publish(pub_topic, "light/usbledoff")
	return home()

################### dht22  ################## 
@app.route('/'+urlDht22)
def getDht22():
	print("dht22");
	mqttc.publish(pub_topic, "sensor/dht22")	
	time.sleep(0.2)
	mqttc.subscribe(subDht22)
	return home()

@app.route('/'+urlDht22_t)
def getDht22_t():
	mqttc.publish(pub_topic, "sensor/dht22_t")
	time.sleep(0.1)
	mqttc.subscribe(subDht22_t)
	return home()

@app.route('/'+urlDht22_h)
def getDht22_h():
	mqttc.publish(pub_topic, "sensor/dht22_h")
	mqttc.subscribe(subDht22_h)
	return home()

################### cds  ######################
@app.route('/'+urlCds)
def getCds():
	mqttc.publish(pub_topic, "sensor/cds")
	mqttc.subscribe(subCds)
	return home()
@app.route('/'+urlPir)
def getPir():
	while True :
		mqttc.subscribe(subPir)
		return render_template('index.html', temperature=temperatureValue, humidity=humidityValue, cds=cdsValue, pir=pirValue)
	return home()
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
	print( str(message))
	print(topic)
	if topic == subDht22 or topic == commonSubDht22 :
		dht22Value = message.split()
		temperatureValue = dht22Value[0]
		humidityValue = dht22Value[1]
	elif topic == subDht22_t or topic == commonSubDht22_t:
		temperatureValue = message
	elif topic == subDht22_h or topic == commonSubDht22_h:
		humidityValue = message
	elif topic == subCds or topic == commonSubCds:
		cdsValue = message
	elif topic == subPir or topic == commonSubPir:
		pirValue = message
	return render_template('index.html', temperature=temperatureValue, humidity=humidityValue, cds=cdsValue, pir=pirValue)
###	print ("Topic: " + topic + " msg: " + message)

def on_connection(mqttc, userdata, flags, rc):
	print("###Connected with result code " + str(rc))
	mqttc.subscribe(subCds)
	return render_template('index.html', temperature=temperatureValue, humidity=humidityValue, cds=cdsValue, pir=pirValue)
		
def checkData():
	mqttc.subscribe(subPir)
	return home() 
if __name__=="__main__":
	mqttc = mqtt.Client("rpi3_1") 
	mqttc.username_pw_set(mqtt_user, mqtt_pwd) 
	mqttc.on_message=on_message 
	mqttc.on_connection=on_connection 
	mqttc.connect(mqtt_broker, 1883, 60) 
	mqttc.loop_start()
	app.run(host="0.0.0.0", port=80, debug=True) 
