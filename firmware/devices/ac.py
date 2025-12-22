from devices.base import IRDevice

class AC(IRDevice):
    def __init__(self, name, ir, codes):
        super().__init__(
            name=name,
            ir=ir,
            codes=codes,
            repeats=3,
            gap_ms=180
        )
