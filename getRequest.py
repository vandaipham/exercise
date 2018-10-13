import requests
import time
import json
from datetime import datetime

ubidots = "http://things.ubidots.com/api/v1.6/devices/demo/Temperature/values?token=A1E-6XrUsrV9jgryqc5B9FyE3W3xMsAlOo"
thingspeak = "https://api.thingspeak.com/channels/72375/feeds.json?results=1"

#payload = {"value": 50}
#url = "http://things.ubidots.com/api/v1.6/devices/demo/Temperature/values/?token=A1E-6XrUsrV9jgryqc5B9FyE3W3xMsAlOo"
#r = requests.post(url, data=payload)
#print(r.text)

thinger = "https://api.thinger.io/v2/users/vandai/devices/esp8266/dht11"
header = {"Authorization":"Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkZXYiOiJlc3A4MjY2IiwiaWF0IjoxNDUwMzA4MDM3LCJqdGkiOiI1NjcxZjFjNTk5MjQyY2ExNmY4MzcyM2MiLCJyZXMiOlsiZGh0MTEiXSwidXNyIjoidmFuZGFpIn0.lrNROrVmTcJkvVQ5CPaWdautsOSyjuOJR2b7a1hA4sU"}

#r = requests.get(thinger, headers=header)
#print (r.text)

file_time = open("file_ubidots.txt", "w")
i = 1

while i < 1001:
	start = datetime.now().timestamp()
#	r = requests.get(thinger, headers=header)
	r = requests.get(ubidots)
	print(r.text)
	delta = datetime.now().timestamp() - start
	print("Response Time = ")
	print(delta)
	file_time.write(str(delta)+ "\n")
	time.sleep(4)
	i+=1
