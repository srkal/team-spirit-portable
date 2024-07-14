import machine
import random
from random import randrange
from machine import Pin
from picodfplayer import DFPlayer
import array, time, utime
from rotary_irq_rp2 import RotaryIRQ

buttonPin = 3
start = time.time()
end = time.time()
# Initialise DFPlayer (UART, TX-Pin, RX-Pin, Busy-Pin)
player = DFPlayer(0, 12, 13, 11)

def shuffle(array):
    "Fisher–Yates shuffle"
    for i in range(len(array)-1, 0, -1):
        j = randrange(i+1)
        array[i], array[j] = array[j], array[i]

def button_callback(pin):
    global start
    global end
    global currentTrackIndex
    global trackOrder
    if pin.value() == 0:
        start = time.time()
    if pin.value() == 1:
        end = time.time()
        elapsed = end - start
        if ((end-start) > 1):
            if (not player.queryBusy()):
               player.playMP3(1000)
        else:
            if (not player.queryBusy()):
               player.playMP3(trackOrder[currentTrackIndex])
               currentTrackIndex = currentTrackIndex + 1
               if currentTrackIndex>=len(trackOrder): currentTrackIndex = 0
               
totalTracks = 13
welcomeTracks = 3

rotary_button = Pin(buttonPin, Pin.IN, Pin.PULL_UP)
encoder = RotaryIRQ(pin_num_clk=1,
              pin_num_dt=2,
              min_val=10,
              max_val=30,
              reverse=True,
              pull_up=True,
              range_mode=RotaryIRQ.RANGE_BOUNDED)

encoder.set(value=23)
player.setVolume(encoder.value())
#welcome sound after switching on
player.playMP3(random.randint(1,welcomeTracks))
while (player.queryBusy()):
    time.sleep_ms(50)

currentTrackIndex = 0
trackOrder = list(range(1+welcomeTracks, totalTracks))
shuffle(trackOrder)
rotary_button.irq(trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING, handler=button_callback)

val_old = encoder.value()
warning_max_volume_played = False
while True:
   try:
     val_new = encoder.value()
     if val_old != val_new:
       val_old = val_new
       print('volume =', val_new)
       player.setVolume(val_new)
     if (val_new == 30):
        if ((not player.queryBusy()) and (not warning_max_volume_played)):
            player.playMP3(1001)
            warning_max_volume_played = True
     else:
        warning_max_volume_played = False
   except KeyboardInterrupt:
     break
