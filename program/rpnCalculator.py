"""
rpnCalculator.py
Kobe Goodwin
"""
from time import sleep_ms
from lcd import LCD
from push_buttons import PushButtons
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
BUTTON_LIST = (("Exponential", "Swap", "0", "Decimal Point", "Add", "B41"),\
               ("Power", "1", "2", "3", "Subtract", "B35"),\
           ("Square", "4", "5", "6", "Multiply", "B29"),\
           ("Scientific Notation", "7", "8", "9", "Divide", "B23"),\
           ("Enter", "Enter", "Reciprocal", "Negate", "Backspace", "Clear"),\
           ("Logarithm", "Power of Ten", "B09", "Arctangent", "Arccosine", "Arcsine"),\
           ("Natural Log", "B02", "B03", "Tangent", "Cosine", "Sine"))


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
            (x,y) = ipHandler.interpretPress(ip, disp,\
                                             BUTTON_LIST)
            lcdScreen.write_at(0,ROWS-2,y)
            lcdScreen.write_at(0,ROWS-1,x)
            lastIp = ip
           
        # A key was released
        elif ip == None:
            lastIp = None
       
        sleep_ms(100)
       
   
       

if __name__ == "__main__":
    main()