"""
rpnCalculator.py
Kobe Goodwin
"""
from machine import Pin
from gpio_lcd import GpioLcd
from time import sleep
import lcd, keypad, pushButtons

PCB = False

# Pinout assignment...
if (PCB == True):
    # LCD    
    COLUMNS = 20
    ROWS = 2
    ST = 22
    SCL = 21
    SDA = 20
    # Button Array
    BUTTON_ROWS = [3, 4, 5, 6, 7, 8, 9]
    BUTTON_COLS = [10, 11, 12, 13, 14, 15]
    BUTTON_LIST = (("B01", "B02", "B03", "B04", "B05", "B06"),\
                ("B07", "B08", "B09", "B10", "B11", "B12"),\
                ("B13", "B13", "B14", "B15", "B16", "B17"),\
                ("B18", "B19", "B20", "B21", "B22", "B23"),\
                ("B24", "B25", "B26", "B27", "B28", "B29"),\
                ("B30", "B31", "B32", "B33", "B34", "B35"),\
                ("B36", "B37", "B38", "B39", "B40", "B41"))
else:
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
    KEYPAD_ROWS = (6,7,8,9)
    KEYPAD_COLS = (10,11,12)
    KEYPAD_LIST = (("1", "2", "3"),\
                   ("4", "5", "6"),\
                   ("7", "8", "9"),\
                   ("*", "0", "#"))
    # Button Array
    BUTTON_ROWS = (0,1,2)
    BUTTON_COLS = (3,4,5)
    BUTTON_LIST = (("A", "B", "C"),\
                   ("D", "E", "F"),\
                   ("G", "H", "I"),\
                   ("J", "K", "L"))
    # Buttons (Direct connection)
    BUTTON_PINS = [16,17,18,19]


def main():
    
    # Keep track of the last input
    lastIp = None
    
    # Initialize I/O
    if (PCB):
        lcdScreen = lcd.Lcd(COLUMNS, ROWS, ST, SCL, SDA)
        buttons = pushButtons.PushButtons(BUTTON_ROWS, BUTTON_COLS, BUTTON_LIST)
    else:
        lcdScreen = lcd.Lcd(COLUMNS, ROWS, RS, E, D4, D5, D6, D7)
        keys = keypad.Keypad(KEYPAD_ROWS, KEYPAD_COLS, KEYPAD_LIST)
        buttons = pushButtons.PushButtons(BUTTON_ROWS, BUTTON_COLS, BUTTON_LIST)
        buttonsDirect = pushButtons.PushButtonsDirect(BUTTON_PINS)
    
    # Initial LCD Output
    if (ROWS > 2):
        lcdScreen.move_cursor(0,0)
        lcdScreen.write("rpnCalculator.py")
        lcdScreen.move_cursor(0,1)
        lcdScreen.write("Kobe Goodwin")
    lcdScreen.move_cursor(0,ROWS-2)
    lcdScreen.write("Y: 0.0000")
    lcdScreen.move_cursor(0,ROWS-1)
    lcdScreen.write("X: 0.0000")
    
    
    while(True):
        # Scan inputs
        ip = buttons.getButton()
        if (ip == None and PCB == False): ip = keys.getKey()
        if (ip == None and PCB == False): ip = buttonsDirect.getButton()

        # A new key is pressed
        if ip != None and ip != lastIp:
            #interpretPress(ip)
            #display()
            print(ip)
            lastIp = ip
            
        # A key was released
        elif ip == None:
            lastIp = None
        
        sleep(0.1)
        
    
        

if __name__ == "__main__":
    main()