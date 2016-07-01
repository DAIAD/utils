from os import listdir
import os
import csv
import json
import time
from datetime import datetime, timedelta
import calendar 
import urllib
import urllib2
import argparse
import random
from random import randint, getrandbits
import time

parser = argparse.ArgumentParser(description='Generate amphiro data.')

parser.add_argument('--device', '-d', type=str, required=True,
                        help='the amphiro device key to assign the generated data to')
parser.add_argument('--username', '-u', type=str, required=True,
                        help='the username with which the device key is associated')
parser.add_argument('--password', '-p', type=str, required=True,
                        help='the user password')
parser.add_argument('--lastId', '-l', type=int, default=0,
                        help='the last shower id for the device key provided (shower ids must be incremental)')
parser.add_argument('--startDate', '-s', type=int, default=int(calendar.timegm(datetime(datetime.now().year, 1, 1).timetuple())),
                        help='the timestamp of the beginning of the period for which data is generated')
parser.add_argument('--endDate', '-e', type=int, default=int(calendar.timegm(datetime.now().timetuple())),
                        help='the timestamp of the end of the period for which data is generated')
parser.add_argument('--output', '-o', type=str, default='out.json',
                        help='the output JSON file')

args = parser.parse_args()

DEVICE_KEY = args.device
USERNAME = args.username
PASSWORD = args.password
FIRST_ID = args.lastId+1
START_DATE = datetime.fromtimestamp(args.startDate)
END_DATE = datetime.fromtimestamp(args.endDate)
OUTPUT = args.output

# helper daterange function
def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)

with open(OUTPUT, 'w') as outfile:
    showers = {
        "deviceKey": DEVICE_KEY,
        "type": "AMPHIRO",
        "credentials": {
                "username": USERNAME,
                "password": PASSWORD,
                },
        "sessions": [],
        "measurements": []
    }
    sessionId = FIRST_ID

    for date in daterange(START_DATE, END_DATE):
        day = date.day
        month = date.month
        year = date.year
        
        print '{0}/{1}/{2}'.format(day, month, year)
         
        # random number of showers per day
        try:
            prev_hour = 0
            numShowers = randint(0, 3)
            for i in range(numShowers):
                print 'shower #', i
                # random hour of day
                hour = randint(prev_hour, 23)
                prev_hour = hour

                timestamp = int(time.mktime(time.strptime('{0}/{1}/{2}T{3}:00:00'.format(day, month, year, hour), '%d/%m/%YT%H:%M:%S'))*1000)
                
                duration = randint(100, 300)
                
                #declaration for scope
                energy = None
                volume = None
                temperature = None
                flow = None

                #last shower of each day is realtime
                if i == numShowers-1:
                    history = False
                else:
                    history = bool(getrandbits(1)) 
                 
                # Real-time 
                if not history:
                    print 'real'

                    energy = randint(20, 30)
                    volume = randint(0, 40)
                    temperature = randint(20, 40)
                    flow = volume / duration
                    
                    measurementstamp = timestamp - duration*1000

                    #separate duration in 10 sec intervals
                    secRange = int(duration/10)
                    
                    for sec in range(secRange):
                        sec += 1
                        menergy = energy
                        mvolume = volume
                        mtemp = temperature + randint(-2, 2)
                        # random energy and volume consumed in interval
                        if sec > 1:
                            menergy = abs(float("{0:.1f}".format(random.uniform(5, 50))))
                            energy += menergy
                            mvolume = abs(float("{0:.1f}".format(random.uniform(2, 15))))
                            volume += mvolume

                        measurement = {
                            "sessionId": sessionId,
                            "index": sec,
                            "history": False,
                            "volume": mvolume, 
                            "energy": menergy,
                            "temperature": mtemp,
                            "timestamp": measurementstamp
                            }
                        
                        print sessionId, sec, mvolume, menergy, mtemp, measurementstamp 
                        
                        measurementstamp += 10*1000

                        showers['measurements'].append(measurement)

                else:
                    print 'historical'

                    flow = randint(7, 15)
                    duration = randint(10*60, 15*60)
                    volume = flow * (duration / 60) 
                    energy = randint(200, 1000)
                    temperature = randint(36, 39)

                print 'total ', volume, energy, flow, duration, temperature
                
                showers['sessions'].append({
                    "id": sessionId,
                    "temperature": temperature,
                    "volume":  "{0:.1f}".format(volume),
                    "energy": "{0:.1f}".format(energy),
                    "flow": flow,
                    "duration": duration,
                    "history": history,
                    "timestamp": timestamp,
                    })

                sessionId += 1

        except Exception as ex:
            print 'exception', ex
            pass
    json.dump(showers, outfile, indent=4)
