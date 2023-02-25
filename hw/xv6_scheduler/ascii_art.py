from art import *


def ascii_art():
    art_1 = art("coffee")  # return art as str in normal mode
    print("a coffee cup for u", art_1)
    Art = text2art("art")  # Return ASCII text (default font) and default chr_ignore=True
    print(Art)
    Art = text2art("art", font='block', chr_ignore=True)  # Return ASCII text with block font
    print(Art)
    Art = text2art("test", "rand")  # random font mode
    print(Art)


if __name__ == '__main__':
    pass
