from .chromatise import *

def add_spaces(val):return val + " " * max(3-len(val),0)

class visual:
    FORE,BACK = "",""

    for x in range(256):
        FORE += ANSI.col_8bit(x) + add_spaces(str(x)) + ANSI.END + ("\n" if(x+1)%16 == 0 else " ")
        BACK += ANSI.col_8bit(x,"back") + add_spaces(str(x)) + ANSI.END + ("\n" if(x+1)%16 == 0 else " ")


