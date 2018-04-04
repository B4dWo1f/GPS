#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import gpxpy
import gpxpy.gpx
from pandas import DataFrame

def gpx(fname,f_out=None,asl=True):
   """
     Returns a pandas.DataFrame from a gpx file.
   asl: True if elevation is given above sea level. False if elevation is given
        above ground
   """
   #try: import gpxpy
   #except: warning
   gpx_file = open(fname, 'r')
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
   columns = ['lon', 'lat', 'ele', 'time']
   return DataFrame(data, columns=columns)


def kml(fname,f_out=None,asl=False):
   """
    Parses a google kml file without any dependence.
    if f_out is an string, write the data to a csv file with format:
      day, month, year, hour, minute, second, lon, lat, height above ground
    Returns a list of points with shape:
             ( (lon,lat,height above ground), date )
   asl: True if elevation is given above sea level. False if elevation is given
        above ground
   """
   lines = open(fname,'r').readlines()
   points = []
   LAT,LON,ELE,TIME = [],[],[],[]
   for i in range(7,len(lines)-4,2):
      date = lines[i].lstrip().rstrip()
      pos = lines[i+1].lstrip().rstrip()
      # Parse position
      print(pos)
      exit()
      aux = list(map(float,pos.split('>')[1].split('<')[0].split()))
      lon,lat,ele = list(map(float,pos.split('>')[1].split('<')[0].split()))
      # Parse date
      D = date.split('>')[1].split('<')[0]
      D = dt.datetime.strptime(D,'%Y-%m-%dT%H:%M:%SZ')
      points.append( (np.array(aux),D) )
      LAT.append(lat)
      LON.append(lon)
      ELE.append(ele)
      TIME.append(D)
      data.append([lon, lat, ele, D])
   #if isinstance(f_out,str):
   #   s = ','
   #   with open(f_out,'w') as f:
   #      for p in points:
   #         r,t = p
   #         t = t.strftime('%d,%m,%Y,%H,%M,%S')
   #         f.write(t+s+str(r[0])+s+str(r[1])+s+str(r[2])+'\n')
   return LAT,LON,ELE #points


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
    f = 'data/flight-2017-11-18-14-59-38.gpx'
    A = gpx2csv(f)
    print(A.describe())
    print(type(A['time'][0]))
    exit()
    fmt = '%d/%m/%Y %H:%M'
    fmt = '%d,%m,%Y,%H,%M,%S'
    A.to_csv('test.csv', date_format=fmt)

