"""
ipHandler.py
Kobe Goodwin 02/11/2025
Map functions to buttons

interpretPress(ip, display)
ip: String representing button input
display: Display instance
Calls button function depending on ip.
Returns (x, y) from display.get()
"""

def interpretPress(ip, display, BUTTON_LIST):
    if (ip == BUTTON_LIST[0][0]): # "B36"
        pass
    elif (ip == BUTTON_LIST[0][1]): # "B37"
        pass
    elif (ip == BUTTON_LIST[0][2]): # "B38"
        display.numberPressed(0)
    elif (ip == BUTTON_LIST[0][3]): # "B39"
        pass
    elif (ip == BUTTON_LIST[0][4]): # "B40"
        display.add()
    elif (ip == BUTTON_LIST[0][5]): # "B41"
        pass
    elif (ip == BUTTON_LIST[1][0]): # "B30"
        pass
    elif (ip == BUTTON_LIST[1][1]): # "B31"
        display.numberPressed(1)
    elif (ip == BUTTON_LIST[1][2]): # "B32"
        display.numberPressed(2)
    elif (ip == BUTTON_LIST[1][3]): # "B33"
        display.numberPressed(3)
    elif (ip == BUTTON_LIST[1][4]): # "B34"
        display.sub()
    elif (ip == BUTTON_LIST[1][5]): # "B35"
        pass
    elif (ip == BUTTON_LIST[2][0]): # "B24"
        pass
    elif (ip == BUTTON_LIST[2][1]): # "B25"
        display.numberPressed(4)
    elif (ip == BUTTON_LIST[2][2]): # "B26"
        display.numberPressed(5)
    elif (ip == BUTTON_LIST[2][3]): # "B27"
        display.numberPressed(6)
    elif (ip == BUTTON_LIST[2][4]): # "B28"
        display.mul()
    elif (ip == BUTTON_LIST[2][5]): # "B29"
        pass
    elif (ip == BUTTON_LIST[3][0]): # "B18"
        pass
    elif (ip == BUTTON_LIST[3][1]): # "B19"
        display.numberPressed(7)
    elif (ip == BUTTON_LIST[3][2]): # "B20"
        display.numberPressed(8)
    elif (ip == BUTTON_LIST[3][3]): # "B21"
        display.numberPressed(9)
    elif (ip == BUTTON_LIST[3][4]): # "B22"
        display.div()
    elif (ip == BUTTON_LIST[3][5]): # "B23"
        pass
    elif (ip == BUTTON_LIST[4][0]): # "B13"
        display.enter()
    elif (ip == BUTTON_LIST[4][1]): # "B13"
        display.enter()
    elif (ip == BUTTON_LIST[4][2]): # "B14"
        pass
    elif (ip == BUTTON_LIST[4][3]): # "B15"
        pass
    elif (ip == BUTTON_LIST[4][4]): # "B16"
        display.backspace()
    elif (ip == BUTTON_LIST[4][5]): # "B17"
        display.clear()
    elif (ip == BUTTON_LIST[5][0]): # "B07"
        pass
    elif (ip == BUTTON_LIST[5][1]): # "B08"
        pass
    elif (ip == BUTTON_LIST[5][2]): # "B09"
        pass
    elif (ip == BUTTON_LIST[5][3]): # "B10"
        pass
    elif (ip == BUTTON_LIST[5][4]): # "B11"
        pass
    elif (ip == BUTTON_LIST[5][5]): # "B12"
        pass
    elif (ip == BUTTON_LIST[6][0]): # "B01"
        pass
    elif (ip == BUTTON_LIST[6][1]): # "B02"
        pass
    elif (ip == BUTTON_LIST[6][2]): # "B03"
        pass
    elif (ip == BUTTON_LIST[6][3]): # "B04"
        pass
    elif (ip == BUTTON_LIST[6][4]): # "B05"
        pass
    elif (ip == BUTTON_LIST[6][5]): # "B06"
        pass
    return display.get()

