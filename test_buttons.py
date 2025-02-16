"""
test_buttons.py
Kobe Goodwin
"""
from machine import Pin
from time import sleep_ms
import lcd, pushButtons
import ipHandler, display

# Pinout assignment...
# LCD    
COLUMNS = 16
ROWS = 2
SCL = 1
SDA = 0
# Button Array
BUTTON_ROWS = [3, 4, 5, 6, 7, 8, 9]
BUTTON_COLS = [10, 11, 12, 13, 14, 15]
BUTTON_LIST = (("B36", "B37", "B38", "B39", "B40", "B41"),\
           ("B30", "B31", "B32", "B33", "B34", "B35"),\
           ("B24", "B25", "B26", "B27", "B28", "B29"),\
           ("B18", "B19", "B20", "B21", "B22", "B23"),\
           ("B13", "B13", "B14", "B15", "B16", "B17"),\
           ("B07", "B08", "B09", "B10", "B11", "B12"),\
           ("B01", "B02", "B03", "B04", "B05", "B06"))


def main():
   
    # Keep track of the last input
    lastIp = None
   
    # Initialize I/O
    lcdScreen = lcd.Lcd(COLUMNS, ROWS, SDA, SCL)
    buttons = pushButtons.PushButtons(BUTTON_ROWS, BUTTON_COLS, BUTTON_LIST)
    disp = display.Display(ROWS, COLUMNS)
   
    # Initial LCD Output
    if (ROWS == 4):
        lcdScreen.write_at(0,0,"rpnCalculator.py")
        lcdScreen.write_at(0,1,"Kobe Goodwin")
    lcdScreen.write_at(0,ROWS-2,"Y: 0")
    lcdScreen.write_at(0,ROWS-1,"X: 0")
   
   
    while(True):
        # Scan inputs
        ip = buttons.getButton()

        # A new key is pressed
        if ip != None and ip != lastIp:
            lcdScreen.write_at(0,ROWS-1,ip)
            lastIp = ip
           
        # A key was released
        elif ip == None:
            lastIp = None
       
        sleep_ms(100)
       
   
       

if __name__ == "__main__":
    main()
