from machine import Pin, PWM
import time
from config import IR_LED_PIN

class IRBlaster:
    CARRIER_FREQ = 38000
    DUTY = 512

    def __init__(self, pin=IR_LED_PIN):
        self.pin = pin
        self._pwm = None

    def _init_pwm(self):
        if self._pwm is None:
            self._pwm = PWM(Pin(self.pin), freq=self.CARRIER_FREQ, duty=0)

    def _on(self):
        self._init_pwm()
        self._pwm.duty(self.DUTY)

    def _off(self):
        if self._pwm:
            self._pwm.duty(0)

    def send(self, code, repeats=1, gap_ms=150):
        """
        code: list of (level, duration_us)
        repeats: how many times to send the full frame
        gap_ms: delay between repeats
        """
        self._init_pwm()

        for i in range(repeats):
            for level, duration in code:
                if level == 0:
                    self._on()
                else:
                    self._off()
                time.sleep_us(duration)

            self._off()

            if i < repeats - 1:
                time.sleep_ms(gap_ms)

