"""
pba_input_breadboard.py
1/4/2024 Kobe Goodwin

Reads input from a 7x6 button array
Prints output to terminal.

GP3-9 -> Rows (Output)
GP10-15 -> Columns (Input)
"""

from machine import Pin
from time import sleep
import lcd, keypad, pushButtons

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
"""
KEYPAD_ROWS = (0,1,2,3,4)
KEYPAD_COLS = (5,6,16,17)
KEYPAD_LIST = (("K01", "K02", "K03","K0A"),\
               ("K04", "K05", "K06","K0B"),\
               ("K07", "K08", "K09","K0C"),\
               ("K0*", "K00", "K0#","K0D"))
"""
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


"""
Scan the button array. Get the button pressed.

(("B01", "B07", "B13", "B19","A","G"),\
("B02", "B08", "B14", "B20","B","H"),\
("B03", "B09", "B15", "B21","C","I"),\
("B04", "B10", "B16", "B22","D","J"),\
("B05", "B11", "B17", "B23","E","K")) 
    
     B01 B07 B13 B19 A B01
     B02 B08 B14 B20 B B02
     B03 B09 B15 B21 C I
     B04 B10 -   B22 D -
     -   -   B17 B23 E K
     


"""
def getButton(col, row):
    # col Input Pins
    # row Output Pins
    for r in row:
        # iteration rows: 011111,101111,110111...
        r.value(0)
        # scan columns
        result = []
        for x in range(0, COLUMNS):
            result = result + [col[x].value()]
        # Where no button is pressed, [1,1,1,1,1,1]
        if min(result) == 0:
            # One of the buttons is pressed! One column is 0
            # Example: Pressing "B01"... result = [0,1,1,1,1,1]
            button = button_list[int(row.index(r))][int(result.index(0))]
            r.value(1)
            return (button)
        # Reset output to 1111
        r.value(1)


"""
Print the button pressed to the terminal
"""
def main():
    
    #lcdScreen = lcd.Lcd(COLUMNS, ROWS, RS, E, D4, D5, D6, D7)
    #keys = keypad.Keypad(KEYPAD_ROWS, KEYPAD_COLS, KEYPAD_LIST)
    buttons = pushButtons.PushButtons(BUTTON_ROWS, BUTTON_COLS, BUTTON_LIST)
    
    # Keep track of the last button
    lastIp = None
    
    while(True):
        
        # Scan inputs
        ip = buttons.getButton()
        #if (ip == None): ip = keys.getKey()
        
        # A new button is pressed
        if ip != None and ip != lastIp:
            #lcdScreen.write_at(0,0,"button: " + str(ip))
            print(ip)
            lastIp = ip
            
        # A button was released
        elif ip == None:
            lastIp = None
            
        sleep(0.1)
        

if __name__ == "__main__":
    main()


