#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import numpy as np

import gpxpy
import gpxpy.gpx

# Parsing an existing file:
# -------------------------
f = 'data/flight-2017-11-18-14-59-38.gpx'
gpx_file = open(f, 'r')
gpx = gpxpy.parse(gpx_file)

data = []
LAT,LON,ELE,TIME = [],[],[],[]
for track in gpx.tracks:
   for segment in track.segments:
      for point in segment.points:
         LAT.append(point.latitude)
         LON.append(point.longitude)
         ELE.append(point.elevation)
         TIME.append(point.time)
         data.append([point.longitude, point.latitude,
                      point.elevation, point.time])

from pandas import DataFrame

columns = ['lon', 'lat', 'ele', 'time']
df = DataFrame(data, columns=columns)
print(df.head())

X = df['lon'].values[1:]
Y = df['lat'].values[1:]
Z = df['ele'].values[1:]
T = df['time'].values[1:]
ele = df['ele'].values
tim = df['time'].values
Vs = []
for i in range(1,len(df['ele'])): #vertical speed
   Vs.append( (ele[i]-ele[i-1])/((tim[i]-tim[i-1]).item()/1e9) )
Vs = np.array(Vs)


#f = 'data.gps'
#Y,X,Z = np.loadtxt(f,delimiter=',',unpack=True)


import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt

#mpl.rcParams['legend.fontsize'] = 10

fig = plt.figure()
ax = fig.gca(projection='3d')

#ax.plot(X, Y, Z)
ax.scatter(X, Y,Z, c=Z,edgecolors='none')
#ax.legend()

plt.show()

