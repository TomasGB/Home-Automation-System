from machine import Pin
import time

class IRReceiver:
    """
    Raw IR receiver.
    Captures (level, duration_us) pairs.
    """

    def __init__(self, pin):
        self.pin = Pin(pin, Pin.IN)

    def capture(self, timeout_us=600_000):
        """
        Waits for IR activity and captures pulses.
        Returns list of (level, duration_us)
        """
        # Wait for signal (idle is usually HIGH)
        start = time.ticks_us()
        while self.pin.value() == 1:
            if time.ticks_diff(time.ticks_us(), start) > timeout_us:
                return None

        pulses = []
        level = self.pin.value()
        t0 = time.ticks_us()

        while True:
            new_level = self.pin.value()
            if new_level != level:
                duration = time.ticks_diff(time.ticks_us(), t0)
                pulses.append((level, duration))
                level = new_level
                t0 = time.ticks_us()

            if time.ticks_diff(time.ticks_us(), t0) > timeout_us:
                break

        return pulses

