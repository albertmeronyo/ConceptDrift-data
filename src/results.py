#!/usr/bin/env python

# Mad results CSV generator

import sys
import csv

inFile = open(sys.argv[1], 'r')
data = inFile.readlines()

results = []

for i,line in enumerate(data):
    if data[i].split()[0] == 'java':
        exp = sys.argv[1]
        mode = "TRAINING"
        if not line.split()[4].split('.')[2] == "meta":
            mode = "TEST"
        # Look if next lines contain results
        if i + 1 < len(data):
            if data[i+1].split()[0] == "Weighted":
                results.append([exp] + [line] + [mode] + data[i+1].split()[2:9])
        if i + 2 < len(data):
            if data[i+2].split()[0] == "Weighted":
                results.append([exp] + [line] + ["10CV"] + data[i+2].split()[2:9])

with open('results.csv', 'wb') as outFile:
    writer = csv.writer(outFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for line in results:
        writer.writerow(line)
