class IRDevice:
    def __init__(self, name, ir, codes, repeats=1, gap_ms=150):
        self.name = name
        self.ir = ir
        self.codes = codes
        self.repeats = repeats
        self.gap_ms = gap_ms

    def send(self, action):
        if action not in self.codes:
            print(f"{self.name}: unknown action {action}")
            return False

        self.ir.send(
            self.codes[action],
            repeats=self.repeats,
            gap_ms=self.gap_ms
        )
        return True
