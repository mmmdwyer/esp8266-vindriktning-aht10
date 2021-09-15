#!/usr/bin/python3

import time
import json
import os
import rrdtool
import os.path
import subprocess
import paho.mqtt.client
import config

# Change to the directory the script is in
homedir=os.path.dirname(os.path.realpath(__file__))
os.chdir(homedir)

filename = 'vindrik.rrd'
lastmessage = {}

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    print(f"Subscribing to {config.mqtttopic}.")
    client.subscribe(config.mqtttopic)

def on_message(client, userdata, msg):
    global lastmessage
    lastmessage = json.loads(str(msg.payload.decode("utf-8")))
    #print("Handling message:",lastmessage)

def create_rrd():
    # If not, but file exists, add to list and exit early
    if os.path.exists(filename):
        #print(f"Using existing {filename}")
        return

    # Otherwise, create a new RRD named this topic
    #  with DataSource lines for each metric.
    # Use these archive definitions:
    # 600 samples of 5 minutes  (2 days and 2 hours)
    # 700 samples of 30 minutes (2 days and 2 hours, plus 12.5 days)
    # 775 samples of 2 hours    (above + 50 days)
    # 797 samples of 1 day      (above + 732 days, rounded up to 797)
    argstring = f'rrdtool create {filename} --start now --step 300'
    for metric in ("pm25","temperature","humidity"):
        argstring += f" DS:{metric}:GAUGE:600:U:U"
    argstring += ' RRA:AVERAGE:0.5:1:600'
    argstring += ' RRA:AVERAGE:0.5:6:700'
    argstring += ' RRA:AVERAGE:0.5:24:775'
    argstring += ' RRA:AVERAGE:0.5:288:797'
    argstring += ' RRA:MAX:0.5:1:600'
    argstring += ' RRA:MAX:0.5:6:700'
    argstring += ' RRA:MAX:0.5:24:775'
    argstring += ' RRA:MAX:0.5:288:797'
    print('Creating new RRD file with these args:')
    print(argstring)
    subprocess.run(argstring.split(" "))

def make_graphs():
    for spec in ( (-86400,"day"),(-604800,"week"),(-2678400,"month"),(-31536000,"year") ):
        rrdtool.graph(f'vindrik{spec[1]}.png', '--start', f'{spec[0]}',
            f'DEF:pm25={filename}:pm25:MAX',
            f'DEF:temp={filename}:temperature:MAX', 
            f'DEF:humi={filename}:humidity:MAX', 
            'LINE1:pm25#00FF00:"PM2.5"',
            'LINE1:temp#FF0000:"Temp C"',
            'LINE1:humi#0000FF:"RH%"')


mqtt = paho.mqtt.client.Client()
mqtt.on_message = on_message
mqtt.on_connect = on_connect
mqtt.connect(config.mqttbrokerhost, config.mqttbrokerport)

nextslot=time.time()+10
nextpaint=time.time()+60

while (True):
    mqtt.loop()
    if ( time.time() > nextslot ):
        nextslot = time.time() + 10  # Slot time to limit writes to RRD
        # print("Timer expired. Running.")
        create_rrd()
        argstring = "N"
        for metric in ("pm25","temperature","humidity"):
            argstring += f":{lastmessage[metric]}"
        rrdtool.update(filename, argstring)
        # print(filename, argstring)
    if (time.time() > nextpaint ):
        nextpaint=time.time()+60
        make_graphs()



