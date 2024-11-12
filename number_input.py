"""
calculator.py
10/29/2024 Kobe Goodwin

Reverse Polish Notation (RPN) Calculator
Raspberry-Pi Pico program

GP0-6 -> 4x3 Keypad (0 to leftmost i/o)
GP16-18 -> K1-K3
"""

from machine import Pin
from time import sleep

num = 0.0000

decimal = 0

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
button4 = Pin(19, Pin.IN)

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
    if (button4.value() == 0):
        sleep(0.1)
        if (button4.value() == 0):
            return "D"
    
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


def numberPressed( number ):
    global num, decimal
    if decimal == 0:
        num = 10*num + number
    else:
        num = num + (number * (10**(-decimal)))
        decimal += 1

def decimalPoint( ):
    global decimal
    if (decimal == 0):
        decimal = 1

def clear( ):
    global num, decimal
    num = 0
    decimal = 0

"""
Given a number pressed, call the appropriate
function.
"""
def interpretPress( key ):
    if (key == "A"):
        print()
    if (key == "B"):
        print()
    if (key == "C"):
        print()
    if (key == "D"):
        print()
    if (key == "1"):
        numberPressed(1)
    if (key == "2"):
        numberPressed(2)
    if (key == "3"):
        numberPressed(3)
    if (key == "4"):
        numberPressed(4)
    if (key == "5"):
        numberPressed(5)
    if (key == "6"):
        numberPressed(6)
    if (key == "7"):
        numberPressed(7)
    if (key == "8"):
        numberPressed(8)
    if (key == "9"):
        numberPressed(9)
    if (key == "*"):
        decimalPoint()
    if (key == "0"):
        numberPressed(0)
    if (key == "#"):
        clear()
    

"""
Print the key pressed to the terminal
"""
def main():
    
    # Keep track of the last key
    lastKey = None
    
    # Display
    print("\n" + str(num))
    
    while(True):
        
        # Scan buttons/keypad
        key = getKey(col_list, row_list)
        
        # A new key is pressed
        if key != None and key != lastKey:
            interpretPress(key)
            print("\n" + str(num))
            lastKey = key
            
        # A key was released
        elif key == None:
            lastKey = None
        
        sleep(0.3)
        
    
        

if __name__ == "__main__":
    main()


