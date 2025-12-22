from devices.base import IRDevice

class TV(IRDevice):
    def __init__(self, name, ir, codes):
        super().__init__(
            name=name,
            ir=ir,
            codes=codes,
            repeats=1
        )
