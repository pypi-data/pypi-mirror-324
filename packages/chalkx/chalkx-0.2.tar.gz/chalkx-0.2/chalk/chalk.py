#github.com/triple7inc
class Dictionary:
    def __init__(self,dictionary):
        for key,value in dictionary.items():
            if isinstance(value,dict):
                value=Dictionary(value)
            self.__dict__[key]=value
    def __getitem__(self,key):
        return(getattr(self,key))
COLORS=Dictionary({
    "black":30,
    "red":31,
    "green":32,
    "yellow":33,
    "blue":34,
    "magenta":35,
    "cyan":36,
    "white":37,
    "grey":90,
    "gray":90,
    "bred":91,
    "bgreen":92,
    "byellow":93,
    "bblue":94,
    "bmagenta":95,
    "bcyan":96,
    "bwhite":97,
})
def chalk(*text,color=None,erase=False):
    """
    Change text color in CMD prompt using ANSI escape codes.

    Parameters:
        text (str): The text to be displayed in the CMD prompt.
        erase (bool): If True, removes previous colors and displays raw text.
        color (str): The name of the desired text color.
                          Valid color names: "black", "red", "green", "yellow",
                          "blue", "magenta", "cyan", "white". You can also use
                          COLORS.black, COLORS.red, etc.

    Returns:
        str: Raw or formatted text with color.
    """
    if erase:
        if isinstance(a,tuple):a="".join(map(str,a))
        a=a.replace("\x1b[0m","")
        for c in COLORS.values():
            a=a.replace(f"\x1b[{c}m","")
        return(a)
    if isinstance(color,int):
        color_code=color
    else:
        try:color_code=COLORS[color]
        except:color_code=37
    a=" ".join(str(a) for a in text)
    return(f"\x1b[{color_code}m{a}\x1b[0m")