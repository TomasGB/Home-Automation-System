# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
#import webrepl
#webrepl.start()

# Minimal startup actions. Kept small — main logic lives in main.py

import machine
import ubinascii
import os

# Optional: create a file marker or reset counters
try:
    machine.freq(240000000)
except Exception:
    pass

# Ensure onboard LED pin is low on boot (safety)
try:
    from machine import Pin
    led = Pin(32, Pin.OUT)
    led.value(0)
except Exception:
    pass

