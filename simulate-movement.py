import time
import sys

filename = 'path.txt'
callsign = 'AHMPOP'
icon = '>'

if len(sys.argv) > 1:
    filename = sys.argv[1]

if len(sys.argv) > 2:
    callsign = sys.argv[2]
    
if len(sys.argv) > 3:
    icon = sys.argv[3]
    
lines = tuple(open(filename, 'r'))

def decdeg2dms(dd):
   is_positive = dd >= 0
   dd = abs(dd)
   minutes,seconds = divmod(dd*3600,60)
   degrees,minutes = divmod(minutes,60)
   degrees = degrees if is_positive else -degrees
   return (degrees,minutes,seconds)

for line in lines:
    line = line.strip()
    latlng = line.split(',')
    lat = float(latlng[0])
    lng = float(latlng[1])
    
    latitude = decdeg2dms(lat)
    longitude = decdeg2dms(lng)

    coordinates = "%02d%02d.%02dN/%03d%02d.%02dE" % (latitude[0], latitude[1], latitude[2], longitude[0], longitude[1], longitude[2])
    raw_packet = "%s%s%s%s" % (callsign, '-5>APDR14,WIDE1-1:=', coordinates, icon)
    print raw_packet
    sys.stdout.flush()
    time.sleep(5)
