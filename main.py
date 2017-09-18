import aprslib
from pprint import pprint
import logging

logging.basicConfig(level=logging.DEBUG) # level=10

i = 0

def dump(obj):
    if type(obj) == dict:
        for k, v in obj.items():
            if hasattr(v, '__iter__'):
                print(k)
                dump(v)
            else:
                print('%s : %s' % (k, v))
    elif type(obj) == list:
        for v in obj:
            if hasattr(v, '__iter__'):
                dump(v)
            else:
                print(v)
    else:
        print(obj)

def callback(packet):
    global i
    try:
        parsed = aprslib.parse(packet)
        #dump(parsed)
        print("heh", i)
        i += 1
    except Exception:
        pass

#LA filter top-left=33.773279, -118.297005, bottom-right=33.509178, -117.812920
#small filter 33.548395, -117.791097 -> 33.534767, -117.778394

AIS = aprslib.IS("N0CALL", port=14580, skip_login=False)
AIS.set_filter("a/34.095565/-118.429184/33.555952/-117.845535") #LA area
#AIS.set_filter("a/43.901711/18.186836/43.797228/18.523293")


#AIS = aprslib.IS("N0CALL")
AIS.connect()
AIS.consumer(callback, raw=True)
