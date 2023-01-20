#!/usr/bin/python

import spidev
import time

#Define Variables
delay = 0.5
pad_channel = 0

#Create SPI
spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz=1000000

from pythonosc import udp_client

client = udp_client.SimpleUDPClient("10.106.50.102",8001)

def mapFromTo(x,a,b,c,d):
    y = (x-a)/(b-a)*(d-c)+c
    return y
    
def readadc(adcnum):
    # read SPI data from the MCP3008, 8 channels in total
    if adcnum > 7 or adcnum < 0:
        return -1
    r = spi.xfer2([1, 8 + adcnum << 4, 0])
    data = ((r[1] & 3) << 8) + r[2]
    return data

try:
    while True:
        pad_value = readadc(pad_channel)
        mappedValue = mapFromTo(pad_value,0,1023,0,360)
        print("---------------------------------------")
        print("Presssure sensor data: %d" % pad_value)
        client.send_message("/pressure",pad_value)
        
        if pad_value > 100 and pad_value < 549:
            client.send_message("/lightpress",pad_value)
            print('lightpress')
        if pad_value > 550:
            client.send_message("/strongpress",pad_value)
            print('strongpress')
            
        #print(mappedValue)
        time.sleep(delay)
        
except KeyboardInterrupt:
    pass
