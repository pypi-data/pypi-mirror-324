from .exceptions import *

class ANSI:
    END = "\033[0m"
    
    def col_8bit(id:int,type:str="fore"):
        if 0 > id or id > 255: raise Invalid8Bit(id)

        type_c = ""
        if type == "fore": type_c = "38;5;"
        elif type == "back": type_c = "48;5;"
        else: raise WrongLayerTypeError(type)
        
        return "\033[%s%sm"%(type_c,str(id))
        
    def col_8bit_rgb(r:int,g:int,b:int,type:str="fore"):
        if 0 > r or r > 255: raise Invalid8Bit(r)
        if 0 > g or g > 255: raise Invalid8Bit(g)
        if 0 > b or b > 255: raise Invalid8Bit(b)

        type_c = ""
        if type == "fore": type_c = "38;2;"
        elif type == "back": type_c = "48;2;"
        else: raise WrongLayerTypeError(type)
        
        return "\033[%s%s;%s;%sm"%(type_c,r,g,b)

    class FORE:
        BLACK = "\033[30m"
        RED = "\033[31m"
        GREEN = "\033[32m"
        BROWN = "\033[33m"
        BLUE = "\033[34m"
        PURPLE = "\033[35m"
        CYAN = "\033[36m"
        LIGHT_GRAY = "\033[37m"
        DARK_GRAY = "\033[30m"
        LIGHT_RED = "\033[31m"
        LIGHT_GREEN = "\033[32m"
        YELLOW = "\033[33m"
        LIGHT_BLUE = "\033[34m"
        LIGHT_PURPLE = "\033[35m"
        LIGHT_CYAN = "\033[36m"
        LIGHT_WHITE = "\033[37m"

    class BACK:
        BLACK = "\033[40m"
        RED = "\033[41m"
        GREEN = "\033[42m"
        BROWN = "\033[43m"
        BLUE = "\033[44m"
        PURPLE = "\033[45m"
        CYAN = "\033[46m"
        LIGHT_GRAY = "\033[47m"
        DARK_GRAY = "\033[40m"
        LIGHT_RED = "\033[41m"
        LIGHT_GREEN = "\033[42m"
        YELLOW = "\033[43m"
        LIGHT_BLUE = "\033[44m"
        LIGHT_PURPLE = "\033[45m"
        LIGHT_CYAN = "\033[46m"
        LIGHT_WHITE = "\033[47m"
    class DECO:
        BOLD = "\033[1m"
        FAINT = "\033[2m"
        ITALIC = "\033[3m"
        UNDERLINE = "\033[4m"
        BLINK = "\033[5m"
        NEGATIVE = "\033[7m"
        CROSSED = "\033[9m"
    