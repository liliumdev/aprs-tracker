import aprslib
import logging

logging.basicConfig(level=logging.DEBUG) # level=10

def callback(packet):
    print(packet)

#LA filter top-left=33.773279, -118.297005, bottom-right=33.509178, -117.812920
#small filter 33.548395, -117.791097 -> 33.534767, -117.778394

AIS = aprslib.IS("N0CALL", port=14580, skip_login=False)
AIS.set_filter("a/59.934954/10.695963/59.896404/10.751925")
AIS.connect()
AIS.consumer(callback, raw=True)
