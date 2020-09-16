import digitalio
from board import *
import time

time.sleep(0.001)




pin4 = digitalio.DigitalInOut(D4)
pin4.direction = digitalio.Direction.OUTPUT

pin17 = digitalio.DigitalInOut(D17)
pin17.direction = digitalio.Direction.INPUT



def distance():  #distance() function to get current
    pin4.value = True
    time.sleep(0.001)
    pin4.value = False

    Start = time.time()
    Stop = time.time()

    while pin17.value = False:
       Start = time.time()
    while pin17.value = True:
       Stop = time.time()
    Epw = Stop- Start
    distance = (Epw*100*(343))/2    # convert to distance
    return distance

while True:
    dis = distance()
    print(dis)
    time.sleep(1)