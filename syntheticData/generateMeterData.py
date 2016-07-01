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
from random import randint, getrandbits
import time

parser = argparse.ArgumentParser(description='Generate SWM data.')

parser.add_argument('--device', '-d', type=str, required=True,
                        help='specific SWM serial to assign the generated data to')
parser.add_argument('--volume', '-v', type=int, default=0,
                        help='the initial SWM volume')
parser.add_argument('--channel', '-ch', type=str, default='VHF',
                        help='the SWM transmission channel type')
parser.add_argument('--company', '-c', type=str, default='AMAEM',
                        help='the water company name')
parser.add_argument('--startDate', '-s', type=int, default=int(calendar.timegm(datetime(datetime.now().year, 1, 1).timetuple())),
                        help='the timestamp of the beginning of the period for which data is generated')
parser.add_argument('--endDate', '-e', type=int, default=int(calendar.timegm(datetime.now().timetuple())),
                        help='the timestamp of the end of the period for which data is generated')
parser.add_argument('--output', '-o', type=str, default='out.csv',
                        help='the output CSV file')

args = parser.parse_args()

METER = args.device
INITIAL_VOLUME = args.volume
CHANNEL = args.channel
COMPANY = args.company
START_DATE = datetime.fromtimestamp(args.startDate)
END_DATE = datetime.fromtimestamp(args.endDate)
OUTPUT = args.output

# helper daterange function
def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)

with open(OUTPUT, 'w') as outfile:
    a = csv.writer(outfile, delimiter=';')

    out = []
    total_volume = INITIAL_VOLUME

    for date in daterange(START_DATE, END_DATE):
        day = date.day
        month = date.month
        year = date.year
        
        try:
            for hour in range(1, 23):
                # random hour of day
                measurement_date = '{0}/{1}/{2} {3}:00:00'.format(day, month, year, hour)
                volume = randint(0, 40)
                total_volume += volume
                row = [CHANNEL, COMPANY, METER, measurement_date, total_volume, volume]
                a.writerow(row)
                    
        except:
            print 'exception'
            pass
