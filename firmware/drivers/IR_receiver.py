from machine import Pin
import time
import ujson
import os

class IRReceiver:
    def __init__(self, pin):
        self.pin = Pin(pin, Pin.IN)

    # -------------------------
    # Capture raw IR pulses
    # -------------------------
    def capture(self, timeout_us=100_000):
        """
        Blocks until a full IR frame is captured.
        Returns: list of [level, duration_us]
        """
        print("IR RX: waiting for signal...")

        # wait for first pulse
        while self.pin.value() == 1:
            pass

        ir_data = []
        level = self.pin.value()
        start = time.ticks_us()

        while True:
            new_level = self.pin.value()
            if new_level != level:
                duration = time.ticks_diff(time.ticks_us(), start)
                ir_data.append([level, duration])
                level = new_level
                start = time.ticks_us()

            # end of frame
            if time.ticks_diff(time.ticks_us(), start) > timeout_us:
                break

        print("IR RX: captured pulses:", len(ir_data))
        return ir_data

    # -------------------------
    # Load / save helpers
    # -------------------------
    def _ensure_dirs(self, path):
        parts = path.split("/")
        current = ""
        for p in parts[:-1]:
            current = f"{current}/{p}" if current else p
            try:
                os.mkdir(current)
            except OSError:
                pass

    def load_codes(self, path):
        try:
            with open(path, "r") as f:
                return ujson.load(f)
        except OSError:
            return {}

    def save_codes(self, path, data):
        self._ensure_dirs(path)
        with open(path, "w") as f:
            ujson.dump(data, f)

    # -------------------------
    # High-level learning API
    # -------------------------
    def learn(self, device_type, model, action):
        """
        Example:
        learn("tv", "samsung", "volume_up")
        """
        path = f"ir_codes/{device_type}/{model}.json"

        codes = self.load_codes(path)

        print(f"Learning IR for {device_type}/{model} -> {action}")
        code = self.capture()

        codes[action] = code
        self.save_codes(path, codes)

        print(f"Saved IR code to {path}")
        return True

