"""
calculator.py
10/29/2024 Kobe Goodwin

Reads input from a 4x3 keypad.
Reads button input.
Prints button/key press to terminal.

GP0-6 -> 4x3 Keypad (0 to leftmost i/o)
GP16-18 -> K1-K3
"""

from machine import Pin
from time import sleep

row_list = [0, 1, 2, 3]  
col_list = [4, 5, 6]

# GP0-3 are output rows set to 1
for x in range(0, 4):
  row_list[x] = Pin(row_list[x], Pin.OUT)
  row_list[x].value(1)

# GP4-6 are input columns
for x in range(0 ,3):
  col_list[x] = Pin(col_list[x], Pin.IN, Pin.PULL_UP)

key_list = [["1", "2", "3"],\
            ["4", "5", "6"],\
            ["7", "8", "9"],\
            ["*", "0", "#"]]

button1 = Pin(16, Pin.IN, Pin.PULL_UP)
button2 = Pin(17, Pin.IN)
button3 = Pin(18, Pin.IN)

"""
Check buttons. Scan the keypad.
Get the key or button pressed.
"""
def getKey(col, row):
    
    # Check buttons. Wait for debouncing.
    if (button1.value() == 0):
        sleep(0.1)
        if (button1.value() == 0):
            return "A"
    if (button2.value() == 0):
        sleep(0.1)
        if (button2.value() == 0):
            return "B"
    if (button3.value() == 0):
        sleep(0.1)
        if (button3.value() == 0):
            return "C"
    
    # col = [GP4, GP5, GP6] Input Pins
    # row = [GP0, GP1, GP2, GP3] Output Pins
    # r = GP0, GP1, GP2, GP3
    for r in row:
        # iteration GP0-3 rows: 0111,1011,1101,1110
        r.value(0)
        # scan GP4-6 columns
        result = [col[0].value(), col[1].value(), col[2].value()]
        # Where no button is pressed, [1,1,1]
        if min(result) == 0:
            # One of the buttons is pressed! One column is 0
            # Example: Pressing "1"... result = [0,1,1]
            # key = key_list[ [GP0, GP1, GP2, GP3].index(GP0)][ [0,1,1].index(0) ]
            # key =	key_list[0][0] = 1
            key = key_list[int(row.index(r))][int(result.index(0))]
            r.value(1)
            return (key)
        # Reset output to 1111
        r.value(1)
        
        
def interpretPress( key ):
    if (key == "A"):
        print("A")
    if (key == "B"):
        print("B")
    if (key == "C"):
        print("C")
    if (key == "1"):
        print(1)
    if (key == "2"):
        print(2)
    if (key == "3"):
        print(3)
    if (key == "4"):
        print(4)
    if (key == "5"):
        print(5)
    if (key == "6"):
        print(6)
    if (key == "7"):
        print(7)
    if (key == "8"):
        print(8)
    if (key == "9"):
        print(9)
    if (key == "*"):
        print("*")
    if (key == "0"):
        print(0)
    if (key == "#"):
        print("#")
    

"""
Print the key pressed to the terminal
"""
def main():
    
    # Keep track of the last key
    lastKey = None
    
    while(True):
        
        # Scan buttons/keypad
        key = getKey(col_list, row_list)
        
        # A new key is pressed
        if key != None and key != lastKey:
            interpretPress(key)
            lastKey = key
            
        # A key was released
        elif key == None:
            lastKey = None
        
        sleep(0.3)
        
    
        

if __name__ == "__main__":
    main()

