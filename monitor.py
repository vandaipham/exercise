import os
import time
import paho.mqtt.client as mqtt
import json

# GET CPU-Temperature
def measure_temp():
	ostemp = os.popen("vcgencmd measure_temp").readline()
	temp = (ostemp.replace("temp=", "").replace("'C\n", ""))
	return temp
#print (measure_temp())

# GET RAM 
# Return RAM information (unit=kb) in a list
# Index 0: total RAM
# Index 1: used RAM
# Index 2: free RAM
def getRAMinfo():
	info = os.popen('free')
	i = 0
	while True:
		i = i + 1
		line = info.readline()
		if i==2:
			return(line.split()[1:4])

#print (getRAMinfo())

# GET CPU # Return % of CPU used by user as a character string
def getCPU():
	return(str(os.popen("top -n1 | awk '/Cpu\(s\):/ {print $2}'").readline().strip()))

#print (getCPU())

# GET Disk Space
# Return information about disk space as a list (unit included)
# Index 0: total disk space 
# Index 1: used disk space 
# Index 2: remaining disk space 
# Index 3: percentage of disk use
def getDisk():
	info = os.popen("df -h /")
	i = 0
	while True:
		i = i+1
		line = info.readline()
		if i==2:
			return(line.split()[1:5])
#print(getDisk())

# MQTT-Client is connecting to Broker
def on_connect(client, userdata, flags, rc):
        if rc == 0:
                print("Connected to broker")
        else:
                print("Connection failed")

def on_publish(client, userdata, result):
        print("data published \n")

client = mqtt.Client("vandai")
client.username_pw_set(username="A1E-aFIT3lYWMKsp0RP2QJJG9om84EHdT4",password=None)
client.on_connect= on_connect
client.on_publish = on_publish

client.connect("things.ubidots.com", 1883, 60)
client.loop_start()


msg = {"temperature":0, "loadcpu":0, "totalram":0, "used-ram":0, "free-ram":0, "total-disk":0, "used-disk":0, "remaining-disk":0, "percentage-of-disk":0}

try:
        while True:
		# read data
                temp = measure_temp()
		ram = getRAMinfo()
		cpu = 100 * float(getCPU())
		disk = getDisk()
		#print (temp)
		#print(ram)
		#print(cpu)
		#print(disk[0].replace("G",""))
		msg["temperature"] = temp
		msg["loadcpu"] = cpu
		msg["totalram"] = 0.001 * float(ram[0])
		msg["used-ram"] = 0.001 * float(ram[1])
		msg["free-ram"] = 0.001 * float(ram[2])
		msg["total-disk"] = disk[0].replace("G","")
		msg["used-disk"] = disk[1].replace("G","")
		msg["remaining-disk"] = disk[2].replace("G","")
		msg["percentage-of-disk"] = disk[3].replace("%","")
		print (msg)
		client.publish("/v1.6/devices/demo", json.dumps(msg))
                time.sleep(5)
except KeyboardInterrupt:
        client.disconnect()
        client.loop_stop()


