#!/usr/bin/env python
#
# GrovePi Example for using the Grove Air Quality Sensor (http://www.seeedstudio.com/wiki/Grove_-_Air_Quality_Sensor)
#
# The GrovePi connects the Raspberry Pi and Grove sensors.  You can learn more about GrovePi here:  http://www.dexterindustries.com/GrovePi
#
# Have a question about this example?  Ask on the forums here:  http://www.dexterindustries.com/forum/?forum=grovepi
#

'''
## License

The MIT License (MIT)

GrovePi for the Raspberry Pi: an open source platform for connecting Grove Sensors to the Raspberry Pi.
Copyright (C) 2015  Dexter Industries

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
'''

# NOTE: # Wait 2 minutes for the sensor to heat-up

import time
import grovepi
import requests
import datetime
import json

# Connect the Grove Air Quality Sensor to analog port A0
# SIG,NC,VCC,GND
air_sensor = 0

grovepi.pinMode(air_sensor,"INPUT")

def mean(values) :
  return sum(values)/len(values)

while True:
        sensor_values_raw = []
        # Get sensor value
        for i in range(0, 5):
          try:
            sensor_values_raw.append(grovepi.analogRead(air_sensor))
            time.sleep(1)
          except IOError:
            print ("Error")

        sensor_value = mean(sensor_values_raw)

        if sensor_value > 700:
            print ("High pollution")
        elif sensor_value > 300:
            print ("Low pollution")
        else:
            print ("Air fresh")

        print ("sensor_value =", sensor_value)

        headers = {'application-id': "XXXX", "secret-key": "XXXX", "Content-Type": "application/json", "application-type": "REST"}
        data={'value': sensor_value, 'date_sent_at': str(datetime.datetime.now())}

        r = requests.post("https://api.backendless.com/v1/data/air_quality", data=json.dumps(data), headers=headers)
        print ( r.text)
