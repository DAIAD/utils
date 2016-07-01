import os
from os.path import basename
import csv
import argparse

parser = argparse.ArgumentParser(description='Extract SWM data from input CSV file.')

parser.add_argument('--input', '-i', type=str, required=True,
    help='input csv file containing SWM data in the expected format with 3 columns: SWM Serial, Measurement date (DD/MM/YYYY HH:MM:SS), total SWM volume')
parser.add_argument('--devices', '-d', type=str, nargs='+', required=True,
                        help='specific real SWM serials from the input file to be extracted')
parser.add_argument('--channel', '-ch', type=str, default='VHF',
                        help='the SWM transmission channel type')
parser.add_argument('--company', '-c', type=str, default='AMAEM',
                        help='the water company name')
parser.add_argument('--output', '-o', type=str, default='out',
                        help='the output folder for the produced CSV files')

args = parser.parse_args()

INPUT = args.input
DEVICES = args.devices
CHANNEL = args.channel
COMPANY = args.company
OUTPUT = args.output

with open(INPUT) as infile:
    reader = csv.reader(infile, delimiter=';')
    diff = 0
    vol = None
    prev = None
    idx = 0
    rowcount = 0

    outfile = open('{0}/{1}.0.csv'.format(OUTPUT, os.path.splitext(basename(INPUT))[0]), 'w')
    writer = csv.writer(outfile, delimiter=';')
    
    for inrow in reader:
      
        device = inrow[0]
        mdate = inrow[1]
        total_vol = inrow[2]

        if not device in DEVICES:
            continue

        if rowcount > 40329:

            outfile.close()
            idx += 1
            rowcount = 0
            outfile = open('{0}/{1}.{2}.csv'.format(OUTPUT, os.path.splitext(basename(INPUT))[0], idx), 'w')
            writer = csv.writer(outfile, delimiter=';')
     
        rowcount += 1
        outrow = []
        outrow.append(CHANNEL)
        outrow.append(COMPANY)
        outrow.append(device)
        outrow.append(mdate)
        outrow.append(total_vol)

        if not prev or not prev == device:
            diff = 0
            vol = int(total_vol)
            prev = device
        else:
            diff = int(total_vol) - vol
            vol = int(total_vol)

        outrow.append(diff)

        writer.writerow(outrow)


        



