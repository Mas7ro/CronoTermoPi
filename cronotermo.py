#!/usr/bin/env python

import RPi.GPIO as GPIO
import time
import Adafruit_DHT

sensor = Adafruit_DHT.DHT11
pin = 4
Temp = 0
Hum = 0

GPIO.setmode(GPIO.BCM)
GPIO.setup(7, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(8, GPIO.OUT, initial=GPIO.LOW)

while True:
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
    if humidity is not None and temperature is not None:
            #print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity))
            Temp = temperature
            Hum = humidity
    else:
            print('Failed to get reading. Try again!')
    # print(Temp)
    print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity))
    if (Temp <= 24):
            GPIO.output(7, GPIO.HIGH)
    elif (Temp >= 25):
            GPIO.output(7, GPIO.LOW)
    if (Hum > 60):
            GPIO.output(8, GPIO.HIGH)
    elif (Hum <= 30):
            GPIO.output(8, GPIO.LOW)
#attivare
#GPIO.output(7, GPIO.HIGH)

    time.sleep(5)

#disattivare
#GPIO.output(7, GPIO.LOW)

#GPIO.cleanup()
