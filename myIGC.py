#!/usr/bin/python3
# -*- coding: UTF-8 -*-

"""
  First draft for a IGC parser
Assumptions:
  - lines are in chronological order
  - The date is the same for every line
"""

import sys
try: fname = sys.argv[1]
except IndexError:
   print('File not specified')
   exit()

import datetime as dt


lines = open(fname,'r').read().splitlines()

FVU_ID = []
fix = []
header = []
for l in lines:
   if l[0] == 'A': FVU_ID.append(l)     # ID number
   elif l[0] == 'B': fix.append(l)      # Fix record
   elif l[0] == 'H': header.append(l)   # Header


## Header
for l in header:
   if 'HFDTE' in l:
      #  HDTE-DD-MM-YY
      Flight_date = dt.date(int(l[9:11])+2000, int(l[7:9]), int(l[5:7]))


# IGC files store latitude as DDMMmmmN
def lat2deg(lat):
   """ Returns the decimal latitude """
   dir_sign = {'N':1, 'S':-1}
   sign = dir_sign[lat[7]]
   degrees = int(lat[0:2])
   minutes = int(lat[2:7]) / 1000.
   return sign * (degrees + minutes/60.)

# IGC files store longitude as DDDMMmmmN
def lon2deg(lon):
   """ Returns the decimal longitude """
   dir_sign = {'E': 1, 'W':-1}
   sign = dir_sign[lon[8]]
   degrees = int(lon[0:3])
   minutes = int(lon[3:8]) / 1000.
   return sign * (degrees + minutes/60.)


## Fix Records
T,Z1,Z2 = [],[],[]
X,Y = [],[]
print('lon,lat,ele')
for l in fix:
   #print(l)
   d = l[1:7]
   d = dt.datetime.combine(Flight_date, dt.time(int(d[0:2]), int(d[2:4]), int(d[4:6]), 0, ))
   lat = lat2deg(l[7:15])
   lon = lon2deg(l[15:24])
   alt_prs = int(l[25:30])
   alt_gps = int(l[30:35])
   ele = (alt_prs+alt_gps)/2
   #print('timestamp:', l[1:7],d)
   #print('      lat,lon:', lat2deg(l[7:15]),lon2deg(l[15:24]))
   ##print('   AVflag:', l[24:25] == "A")
   #print(' pressure:', int(l[25:30]))
   #print('  alt-GPS:', int(l[30:35]))
   X.append(lon)
   Y.append(lat)
   T.append(d)
   Z1.append(int(l[25:30]))
   Z2.append(int(l[30:35]))
   print('%s,%s,%s'%(lon,lat,ele))
      #exit()

#print(min(X),max(X))
#print(min(Y),max(Y))
exit()
import matplotlib.pyplot as plt
fig, ax = plt.subplots()
ax.plot(T,Z1,label='press')
ax.plot(T,Z2,label='gps')
ax.legend()
plt.show()
