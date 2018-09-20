import aprslib
import hashlib
from pprint import pprint
import logging
import json
import requests
import threading
import sys
import argparse

i = 0

class Tracker:
    api_url = 'http://aprs/'
    name = 'Unknown tracker'
    do_ping = True
    lat_from = 0
    lat_to = 90
    long_from = 0
    long_to = 180
    packets_received = 0
    packets_lost = 0
    tracked_properties = ['latitude', 'longitude', 'altitude', 'from', 'to',
                        'format', 'symbol', 'symbol_table', 'comment',
                        'object_name', 'speed', 'message_text', 'raw']
    listenStdin = False

    def __init__(self, name, geo_constraints, listenStdin=False):
         self.name = name
         self.lat_from  = geo_constraints['lat_from']
         self.lat_to    = geo_constraints['lat_to']
         self.long_from = geo_constraints['long_from']
         self.long_to   = geo_constraints['long_to']
         self.listenStdin = listenStdin

    def track(self, filter=True):
        self.ping()
        if self.listenStdin:
            print "Listening to stdin ..."
            while True:
                raw_packet = sys.stdin.readline().strip()
                if raw_packet:
                    self.packet_received(raw_packet)
        else:
            print "Listening to APRS-IS"
            AIS = None
            if filter:
                print("Setting filter...")
                AIS = aprslib.IS("N0C4LL", port=14580, skip_login=False)
                AIS.set_filter("a/{}/{}/{}/{}".format(self.lat_from, self.long_from,
                                                      self.lat_to, self.long_to))
            else:
                AIS = aprslib.IS("N0C4LL")
                
            AIS.connect()
            AIS.consumer(self.packet_received, raw=True)        

    def ping(self):
        if self.do_ping:
            print('Pinging...')
            
            next_ping = threading.Timer(25.0, self.ping)
            next_ping.daemon = True
            next_ping.start()
            
            data = {
                'name': self.name,
                'lat_from':  self.lat_from,
                'lat_to':    self.lat_to,
                'long_from': self.long_from,
                'long_to':  self.long_to
                }
            
            response = requests.post(self.api_url + 'ping', json=data)

    def packet_received(self, raw_packet):
        self.packets_received += 1

        try:
            packet = self.parse_packet(raw_packet)
            print('Packet #{} received'.format(self.packets_received))
            response = requests.post(self.api_url + 'store', json=packet)
            print(response.text)
        except Exception as e:
            self.packets_lost += 1
            print('Packet lost due to unknown format or unsupported parsing')
            pass

    def parse_packet(self, raw_packet):        
        md5 = hashlib.md5()
        md5.update(raw_packet)
        packet_hash = md5.hexdigest()
        parsed_packet = {'hash': packet_hash}
            
        packet = aprslib.parse(raw_packet)
        for key in self.tracked_properties:
            parsed_packet[key] = self.get_property(packet, key)

        return parsed_packet
    
    def get_property(self, packet, key):
        if key in packet:
            return packet[key]

        return ''                  

# Bosnia
#t = Tracker("Bosnian tracker @ Pofalici", {
#    'lat_from':   45.7905094,
#    'lat_to':     42.0370543,
#    'long_from':  13.1616210,
#    'long_to':    23.7084960
#    })

# Dusseldorf
#t = Tracker("Ahmed's tracker @ Pofalici", {
#    'lat_from':  51.293150,
#    'lat_to':    51.142464,
#    'long_from': 6.605873,
#    'long_to':   6.9493685
#    })

parser = argparse.ArgumentParser()
parser.add_argument('--mode', '-m', help='One of \'aprs-is\' or \'stdin\' - denotes does the script connect to APRS-IS or wait for stdin input.', type= str)

print parser.format_help()
print ""

args = parser.parse_args()

mode = 1 # Default is APRS-IS

if args.mode == 'aprs-is':
    mode = 1
elif args.mode == 'stdin':
    mode = 2

if mode == 1:
     t = Tracker("Ahmed's world tracker", {
    'lat_from':  45.7905094,
    'lat_to':    42.0370543,
    'long_from': 13.1616210,
    'long_to':   23.7084960
    })
else:
    t = Tracker("Ahmed's world tracker", {
    'lat_from':  0,
    'lat_to':    0,
    'long_from': 0,
    'long_to':   0
    }, True)
    

while True:
    try:    
        print("Starting ...")
        t.track(False)
        print("Started.")
    except KeyboardInterrupt:
        print("Closing ...")
        t.do_ping = False
        break
    except aprslib.exceptions.ConnectionDrop:
        pass
    except aprslib.exceptions.ConnectionError:
        pass

