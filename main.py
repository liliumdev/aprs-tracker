# Ova skripta dijeli mapu svijeta na tzv. zone i kreira MySQL kod spreman za importovanje
# Dakle, mapa svijeta se dijeli na kvadratnu mrežu kako bi mogli grupirati / izvršiti clustering
# nad velikim datasetom kojeg bi bilo nemoguće fino prikazati pri malom zoomu.

# Otprilike, planirano je da :
#   nivo zooma 0-4 -> mreža od 16 ćelija/zona (dakle mreža dimenzije 4),
#   nivo zooma 5-7 -> mreža od 32 zone (dimenzija 5)
#   nivo zooma 8+  -> nema mreže

min_lat = -90
max_lat = 90
min_long = -180
max_long = 180

dimension = 4

lat_step = 180/dimension
long_step = 360/dimension

from_lat = min_lat

for i in range(0, dimension):
    to_lat = from_lat + lat_step
    from_long = min_long
    for j in range(0, dimension):
        to_long = from_long + long_step
        center_lat = (from_lat + to_lat) / 2
        center_long = (from_long + to_long) / 2

        print(from_lat, to_lat, ",", from_long, to_long, " | center: ", center_lat, center_long)
        from_long += long_step
        if from_long > 180:
            from_long = min_long

    from_lat += lat_step
    if from_lat > 90:
        from_lat = min_lat
