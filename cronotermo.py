#!/usr/bin/python
# encoding: UTF-8
"""
CronoTermoPi v0.1
Programma in Python (sviluppato su Raspberry Pi zero w) per la gestione di un impianto
di riscaldamento e di condizionamento con monitoraggio e gestione via Blynk su Android.

Il programma è sviluppato principalmente per esigenze personali per una villa al
mare. D'inverno deve accendere la caldaia e riscaldare la casa, e, all'occorrenza,
accendere il deumidificatore, per un paio di ore a settimana, e devo poter
comandarne l'accensione quando decido di andare nel w.e.. Inizialmente questi
parametri verranno inseriti nel codice, prevedendo poi di spostarli su file o
database. Cercherò di tenere presente una programmazione quanto piu flessibile
possibile

  Downloads, docs, tutorials: https://github.com/Mas7ro/CronoTermoPi

Considero due macrovariabili, Stagione e Stato. La stagione è intendo o estiva
o invernale, lo Stato sarà On oppure Off. D'inverno se lo Stato è On accende il
riscaldamento e porta la casa a Tmax, se invece Stato è Off accenderà la caldaia
solo se la temperatura scende sotto Tmin.
Questa è la parte che piu mi interessa e parto con lo sviluppo di questa.

"""
# import pdb
import BlynkLib
import RPi.GPIO as GPIO
import time
import Adafruit_DHT
import os
try:
	while True:
            # pdb.set_trace()

            BLYNK_AUTH = 'Token'
            # initialize Blynk
            blynk = BlynkLib.Blynk(BLYNK_AUTH)

            sensor = Adafruit_DHT.DHT11
            pin = 4
            Temp = 0
            Hum = 0
            rele1 = 0 # serve per visualizzare sul grafico di blynk l'accensione della caldaia

            # --- Variabili di configurazione (da mettere in file esterno o db)---
            Stagione = 0  # 0 = inverno, 1 = estate
            Stato = 0  # 1 Attivo, 0 non attivo
            TempMax = 23
            TempMin = 19
            TempEstate = 27
            TempDiff = 0.5
            # --- FINE variabili di configurazione ---

            GPIO.setwarnings(False)
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(7, GPIO.OUT, initial=GPIO.LOW) # relays accensione caldaia
            # GPIO.setup(8, GPIO.OUT, initial=GPIO.LOW) # relays accensione ventilatore

            # Return CPU temperature as a character string
            def getCPUtemperature():
                res = os.popen('vcgencmd measure_temp').readline()
                return(res.replace("temp=", "").replace("'C\n", ""))


            CPU_temp = getCPUtemperature()


            # register the task running every 3 sec
            # (period must be a multiple of 50 ms)
            def my_user_task():
                # do any non-blocking operations
                global rele1
                humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
                if humidity is not None and temperature is not None:
                        # print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature,
                        # humidity))
                        Temp = int(temperature)
                        Hum = humidity
                else:
                        print('Failed to get reading. Try again!')

                @blynk.VIRTUAL_WRITE(6)
                def v6_write_handler(buttonstatus):
                    global Stato
                    # print('Current Stato value: {}'.format(buttonstatus))
                    # print(buttonstatus)
                    if buttonstatus is not None:
                        Stato = int(buttonstatus)
                        # print type(buttonstatus)
                # print Temp, '*C'
                # print Hum, '%'
                # print Temp, TempMax - TempDiff, Stato, Stagione
                # print Temp < TempMax - TempDiff and Stato == 1 and Stagione == 0
                # print Temp >= TempMax and Stato == 1 and Stagione == 0
                # print Temp < (TempMax - TempDiff) and Stato == 0 and Stagione == 0
                # print Temp < TempMin and Stagione == 0 and Stato == 0
                # print Temp > (TempMin + TempDiff) and Stagione == 0 and Stato == 0
                # print Stato
                if (Temp < TempMax - TempDiff and Stato == 1 and Stagione == 0):
                    GPIO.output(7, GPIO.HIGH)
                    rele1 = 255
                elif (Temp >= TempMax and Stato == 1 and Stagione == 0):
                    GPIO.output(7, GPIO.LOW)
                    rele1 = 0
                    # print(rele1)
                elif (Temp < TempMax - TempDiff and Stato == 0 and Stagione == 0):
                    GPIO.output(7, GPIO.LOW)
                    rele1 = 0
                elif (Temp < TempMin and Stagione == 0 and Stato == 0):
                    GPIO.output(7, GPIO.HIGH)
                    rele1 = 255
                elif (Temp > (TempMin + TempDiff) and Stagione == 0 and Stato == 0):
                    GPIO.output(7, GPIO.LOW)
                    rele1 = 0
                blynk.virtual_write(2, Temp)
                blynk.virtual_write(3, Hum)
                blynk.virtual_write(4, CPU_temp)
                blynk.virtual_write(5, rele1)
                blynk.virtual_write(6, Stato)
                if Stato == 1:
                    blynk.virtual_write(7, 255)
                elif Stato == 0:
                    blynk.virtual_write(7, 0)


            blynk.set_user_task(my_user_task, 3000)

            # start Blynk (this call should never return)
            blynk.run()
except KeyboardInterrupt:
	GPIO.cleanup()
