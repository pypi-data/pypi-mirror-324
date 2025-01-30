class WrongLayerTypeError(Exception):
    def __init__(self,wrongType):
        self.message = "Parameter %s passed, \'fore\' or \'back\' expected"%wrongType
        super().__init__(self.message)

class Invalid8Bit(Exception):
    def __init__(self,num):
        self.message = "Integer argument(s) should be in 8-bit range (0-255)"
        super().__init__(self.message)