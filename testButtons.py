"""
rpnCalculator.py
Kobe Goodwin
"""
from machine import Pin
from gpio_lcd import GpioLcd
from time import sleep
import lcd, keypad, pushButtons
import ipHandler, number, display


# LCD
COLUMNS = 20
ROWS = 4
RS = 28
E = 27
D4 = 26
D5 = 22
D6 = 21
D7 = 20
# Keypad
KEYPAD_ROWS = (0,1,2,3)
KEYPAD_COLS = (4,5,6)
KEYPAD_LIST = (("1", "2", "3"),\
               ("4", "5", "6"),\
               ("7", "8", "9"),\
               ("*", "0", "#"))
# Button Array
BUTTON_ROWS = (14,15,13)
BUTTON_COLS = (11,10,12)
BUTTON_LIST = (("A", "B", "C"),\
               ("D", "E", "F"),\
               ("G", "H", "I"),\
               ("J", "K", "L"))
# Buttons (Direct connection)
BUTTON_PINS = (16,17,18,19)

def main():
    
    # Keep track of the last input
    lastIp = None
    
    lcdScreen = lcd.Lcd(COLUMNS, ROWS, RS, E, D4, D5, D6, D7)
    keys = keypad.Keypad(KEYPAD_ROWS, KEYPAD_COLS, KEYPAD_LIST)
    buttons = pushButtons.PushButtons(BUTTON_ROWS, BUTTON_COLS, BUTTON_LIST)
    buttonsDirect = pushButtons.PushButtonsDirect(BUTTON_PINS)
    disp = display.Display(ROWS, COLUMNS)
    
    # Initial LCD Output
    if (ROWS > 2):
        lcdScreen.write_at(0,0,"testButtons.py")
        lcdScreen.write_at(0,1,"Kobe Goodwin")
    
    while(True):
        # Scan inputs
        ip = buttons.getButton()
        if (ip == None): ip = keys.getKey()
        if (ip == None): ip = buttonsDirect.getButton()

        # A new key is pressed
        if ip != None and ip != lastIp:
            lcdScreen.write_at(0,ROWS-1,ip)
            lastIp = ip
            
        # A key was released
        elif ip == None:
            lastIp = None
        
        sleep(0.1)
        
    
        

if __name__ == "__main__":
    main()
