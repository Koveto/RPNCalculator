"""
pba_input.py
12/20/2024 Kobe Goodwin

Reads input from a 7x6 button array
Prints output to terminal.

GP3-9 -> Rows (Output)
GP10-15 -> Columns (Input)
"""

from machine import Pin
from time import sleep

ROWS = 7
COLUMNS = 6

row_list = [3, 4, 5, 6, 7, 8, 9]
col_list = [10, 11, 12, 13, 14, 15]

button_list = (("B01", "B02", "B03", "B04", "B05", "B06"),\
            ("B07", "B08", "B09", "B10", "B11", "B12"),\
            ("B13", "B13", "B14", "B15", "B16", "B17"),\
            ("B18", "B19", "B20", "B21", "B22", "B23"),\
            ("B24", "B25", "B26", "B27", "B28", "B29"),\
            ("B30", "B31", "B32", "B33", "B34", "B35"),\
            ("B36", "B37", "B38", "B39", "B40", "B41"))

# Output set
for x in range(0, ROWS):
  row_list[x] = Pin(row_list[x], Pin.OUT)
  row_list[x].value(1)

# Input defined
for x in range(0 ,COLUMNS):
  col_list[x] = Pin(col_list[x], Pin.IN, Pin.PULL_UP)


"""
Scan the button array. Get the button pressed.
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
    
    # Keep track of the last button
    lastButton = None
    
    while(True):
        
        # Scan array
        button = getButton(col_list, row_list)
        
        # A new button is pressed
        if button != None and button != lastButton:
            print("button: "+str(button))
            lastButton = button
            
        # A button was released
        elif button == None:
            lastButton = None
            
        sleep(0.1)
        

if __name__ == "__main__":
    main()

