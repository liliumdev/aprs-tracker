lines = tuple(open('path.txt', 'r'))

callsign = 'AHMPOP-5'
icon = '>'

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
