#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import itertools
from datetime import datetime, timedelta
from dateutil.parser import parse

f = open('versions.json', 'r')
a = json.load(f)

dsGaps = []
for ds, versions in a.iteritems():
    dates = []
    for v in versions:
        dates.append(v[0])
    sortedDates = sorted(dates)
    daysGap = 0
    for firstDate, secondDate in itertools.izip(sortedDates, sortedDates[1:]):
        firstDate = parse(firstDate)
        secondDate = parse(secondDate)
        daysGap += (secondDate - firstDate).days
    if len(sortedDates) > 2:
        dsGaps.append([ds, float(daysGap) / (len(sortedDates) - 1)])
for ds in sorted(dsGaps, key=lambda x: x[0]):
    print ds[0], ds[1]


