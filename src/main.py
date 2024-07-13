import machine
import random
from machine import Pin
from picodfplayer import DFPlayer
import array, time, utime
from rotary_irq_rp2 import RotaryIRQ

rotary_button = Pin(3, Pin.IN, Pin.PULL_UP)

encoder = RotaryIRQ(pin_num_clk=1,
              pin_num_dt=2,
              min_val=10,
              max_val=30,
              reverse=True,
              pull_up=True,
              range_mode=RotaryIRQ.RANGE_BOUNDED)

encoder.set(value=23)

# Initialise DFPlayer (UART, TX-Pin, RX-Pin, Busy-Pin)
player = DFPlayer(0, 12, 13, 11)
player.setVolume(encoder.value())
time.sleep(0.1)
#initial sound after switching on
player.playMP3(2)
while (player.queryBusy()):
    time.sleep_ms(50)

#print(player.queryBusy())
val_old = encoder.value()
while True:
   try:
     val_new = encoder.value()
     if rotary_button.value()==0:
       print("Button Pressed")
       if (not player.queryBusy()):
           player.playMP3(random.randint(3,10))
       print("Selected volume is : ",val_new)
     if val_old != val_new:
       val_old = val_new
       print('volume =', val_new)
       player.setVolume(val_new)
     time.sleep_ms(50)
   except KeyboardInterrupt:
     break
