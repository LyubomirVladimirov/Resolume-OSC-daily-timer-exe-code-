
from oscpy.client import OSCClient
from collections import defaultdict
from datetime import datetime
import pandas as pd
import csv
import os
from dateutil.parser import parse
import time


external_config = pd.read_csv('config.csv')
external_ip_config = pd.read_csv('ip_config.csv')

m = len(external_ip_config)
n = len(external_config)

if m == 0:
    print ("ip_config file is Empty!")

    print ("Exiting in 5 sec...")
    time.sleep(5)
    exit()

if n == 0:
    print ("config file is Empty!")

    print ("Exiting in 5 sec...")
    time.sleep(5)
    exit()

marker = [] 
target_hour = []
target_minute = []
string_container = []
value_container = []

for z in range(n):
    marker.append(0)

print external_config
print external_ip_config 

ip = str(external_ip_config['ip'][0])
port = int(external_ip_config['port'][0])

for x in range(n):
    target_hour.append(int(external_config['hour'][x]))
    target_minute.append(int(external_config['minute'][x]))
    string_container.append(str(external_config['string'][x]))
    value_container.append(float(external_config['value'][x])) 

print ("Running...")
while(1):
    time.sleep(1)
    date = parse(str(datetime.now()))
    hour_now = str(date.hour)
    minute_now = str(date.minute)

    for x in range(n):
        if int(target_hour[x]) == int(hour_now) and int(target_minute[x]) == int(minute_now) and marker[x] == 0:
            print ("event " + str(x+1) + " triggered")
            osc = OSCClient(str(ip), port)
            print('Sending ...')
            for y in range(10):
                osc.send_message(str(string_container[x]), [value_container[x]])
            print('Sent 10 times.')                              
            marker[x] = 1
            time.sleep(1)
        elif int(target_hour[x]) != int(hour_now) or int(target_minute[x]) != int(minute_now):
            marker[x] = 0
        

