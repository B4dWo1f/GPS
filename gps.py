#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from math import sin, cos, atan2, sqrt, radians
import datetime as dt

def deg2dec(deg,minu,sec):
   """ Converts degree, minute, second to decimal """
   return deg + minu/60. + sec/3600.

def degd2dec(deg,minu,sec,d):
   """ Same as deg2dec including direction {'N','E','S','W'} """
   NSEW = {'E':1, 'N':1, 'S':-1, 'W':-1}
   value = deg2dec(deg,minu,sec)
   sign = NSEW[d]
   return sign * value

def points2distance(start, end, R0=6371):
   """
    Calculate distance (in kilometers) between two points given as
    (long, latt) pairs based on Haversine formula:
          http://en.wikipedia.org/wiki/Haversine_formula
    R0 = 6371km is the radious of the earth
   """
   ## Degrees to Radians
   start_long = radians(start[0])  # Start point
   start_latt = radians(start[1])  #
   end_long = radians(end[0])  # End point
   end_latt = radians(end[1])  #
   d_long = end_long - start_long
   d_latt = end_latt - start_latt
   a = sin(d_latt/2)**2 + cos(start_latt) * cos(end_latt) * sin(d_long/2)**2
   c = 2 * atan2(sqrt(a), sqrt(1-a))
   return R0 * c

def date2timestamp(fecha,epoch=dt.datetime(1970, 1, 1)):
   """ Returns the UNIX timestamp for a given date """
   timestamp = (fecha - epoch) // dt.timedelta(seconds=1) # Integer
   return timestamp #(dt - epoch) // dt.timedelta(seconds=1)


def read_csv(fname):
   """
    Read from csv file with format:
       day, month, year, hour, minute, second, lon, lat, height above ground
    Returns a list of points with shape:
              ( (lon,lat,height above ground), date )
   """
   D,M,Y,h,m,s,lon,lat,alt = np.loadtxt(fname,delimiter=',',unpack=True)
   points = []
   for i in range(len(lat)):
      date = (int(Y[i]),int(M[i]),int(D[i]),int(h[i]),int(m[i]),int(s[i]))
      date = dt.datetime(*date)
      points.append( (np.array([lat[i],lon[i],alt[i]]),date) )
   return points

if __name__ == '__main__':
    #f = 'data/flight-2017-11-18-14-59-38.gpx'
    f = 'data/Historialdeubicaciones.kml'
    #A = gpx2csv(f)
    #print(A.describe())
    #print(type(A['time'][0]))
    #exit()
    #fmt = '%d/%m/%Y %H:%M'
    #fmt = '%d,%m,%Y,%H,%M,%S'
    #A.to_csv('test.csv', date_format=fmt)
    import IO
    IO.kml(f)
