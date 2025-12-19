# drivers/dht_driver.py
import time
try:
    import dht
    from machine import Pin
except Exception:
    dht = None

class DHTDriver:
    def __init__(self, pin):
        self._pin = pin
        self._sensor = None
        if dht:
            try:
                self._sensor = dht.DHT11(Pin(pin))
            except Exception:
                self._sensor = None

    def read(self):
        """Return (temperature, humidity) or (None, None) on failure."""
        if not self._sensor:
            return None, None
        try:
            self._sensor.measure()
            t = self._sensor.temperature()
            h = self._sensor.humidity()
            # DHT11 returns ints; convert to float for consistency
            return float(t), float(h)
        except Exception:
            return None, None
