# -*- coding: utf-8 -*-
"""
Created on Wed Feb 17 10:29:13 2016

@author: doug
"""

import os 
import csv
import datetime
import numpy as np

dirLoc = "S:\\Dougs_Documents\\gDrive\\random other\\"
fileBase = "Portfolio_Position_"

todayDate = datetime.date.today()

fileName = dirLoc + fileBase + todayDate.strftime("%b-%d-%Y") + ".csv"
rowNum = 0
symbols = []
values = []

with open(fileName) as csvfile:
    fileRead = csv.reader(csvfile, delimiter=',')
    for row in fileRead:
        if row == []:
            break
        rowNum += 1        
        if rowNum == 1:
            symIndex = row.index('Symbol')
            valIndex = row.index('Current Value')
        else:
            symbols.append(row[symIndex])
            values.append(float(row[valIndex][1:]))
    csvfile.close

totalVal = sum(values)
props = []
cashAvail = 0

for i in range(0,len(symbols)):
    if symbols[i]=="FDRXX**":
        props.append(0)
        cashAvail = values[i]
        print "total cash available: $" + str(cashAvail)
    else:
        if abs(0.3 * totalVal - values[i]) < abs(0.1 * totalVal - values[i]):
            props.append(0.3)
        else:
            props.append(0.1)

symbols = np.array(symbols)
values = np.array(values)
props = np.array(props)
            
targetVals = np.round(totalVal * props, 2)
diff = np.array(targetVals - values)
cashAlloc = np.zeros_like(diff)
diff = diff * (diff > 0)

while cashAvail > 0:
    props = (props * (diff > 0) / np.sum(props * (diff >0)))    
    thisAlloc = np.round(cashAvail * props, 2)
    if np.all(thisAlloc == np.minimum(thisAlloc, diff)):
        cashAlloc = cashAlloc + thisAlloc
        cashAvail -= np.sum(thisAlloc)
        cashAvail = round(cashAvail, 2)
        break
    else:
        thisAlloc = np.minimum(thisAlloc, diff)
        cashAlloc += thisAlloc
    diff = diff - thisAlloc
    cashAvail -= np.sum(thisAlloc)
    cashAvail = round(cashAvail, 2)
    
for i in range(0,len(symbols)):
    print "----------"    
    if symbols[i]=="FDRXX**":
        print symbols[i] + " - Unallocated Cash"
        print "     " + str(cashAvail)
    else:
        if cashAlloc[i] > 0:
            print "BUY " + symbols[i]
            print "     $" + str(cashAlloc[i])
        else:
            print "NO ACTION ON " + symbols[i]
