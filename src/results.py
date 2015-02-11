#!/usr/bin/env python

# Mad results CSV generator

import sys
import csv

inFile = open(sys.argv[1], 'r')

results = []

for i,line in enumerate(inFile.readlines()):
    if line.split()[0] == 'java':
        # Look if next lines contain results
        if line[i+1].split()[0] == "Weighted":
            results.append([line + line[i+1].split()[2:9]])
        if line[i+2].split()[0] == "Weighted":
            results.append([line + line[i+2].split()[2:9]])

with open('results.csv') as outFile:
    writer = csv.writer(outFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for line in results:
        writer.writerow(line)

    
