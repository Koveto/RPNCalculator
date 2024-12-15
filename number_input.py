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
import cmath

num = 0   # real
num1 = 0  # imag

decimal = 0
exp = False
compl = False

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

buttonA = Pin(19, Pin.IN, Pin.PULL_UP)
buttonB = Pin(18, Pin.IN)
buttonC = Pin(17, Pin.IN)
buttonD = Pin(16, Pin.IN)
buttonE = Pin(20, Pin.IN)
buttonF = Pin(21, Pin.IN)
buttonG = Pin(22, Pin.IN)
buttonH = Pin(26, Pin.IN)
buttonI = Pin(27, Pin.IN)
buttonJ = Pin(28, Pin.IN)																																		
buttonK = Pin(15, Pin.IN)
buttonL = Pin(14, Pin.IN)

"""
Check buttons. Scan the keypad.
Get the key or button pressed.
"""
def getKey(col, row):
    
    # Check buttons. Wait for debouncing.
    if (buttonA.value() == 0):
        sleep(0.1)
        if (buttonA.value() == 0):
            return "A"
    if (buttonB.value() == 0):
        sleep(0.1)
        if (buttonB.value() == 0):
            return "B"
    if (buttonC.value() == 0):
        sleep(0.1)
        if (buttonC.value() == 0):
            return "C"
    if (buttonD.value() == 0):
        sleep(0.1)
        if (buttonD.value() == 0):
            return "D"
    if (buttonE.value() == 0):
        sleep(0.1)
        if (buttonE.value() == 0):
            return "E"
    if (buttonF.value() == 0):
        sleep(0.1)
        if (buttonF.value() == 0):
            return "F"
    if (buttonG.value() == 0):
        sleep(0.1)
        if (buttonG.value() == 0):
            return "G"
    if (buttonH.value() == 0):
        sleep(0.1)
        if (buttonH.value() == 0):
            return "H"
    if (buttonI.value() == 0):
        sleep(0.1)
        if (buttonI.value() == 0):
            return "I"
    if (buttonJ.value() == 0):
        sleep(0.1)
        if (buttonJ.value() == 0):
            return "J"
    if (buttonK.value() == 0):
        sleep(0.1)
        if (buttonK.value() == 0):
            return "K"
    if (buttonL.value() == 0):
        sleep(0.1)
        if (buttonL.value() == 0):
            return "L"
    
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
    global num, num1, decimal, compl, exp
    if exp:
        num = num * (10 ** (number))
        exp = False
    else:
        if decimal == 0:
            if not compl:
                num = 10*num + number
            else:
                num1 = 10*num1 + number
        else:
            if not compl:
                num = num + (number * (10**(-decimal)))
            else:
                num1 = num1 + (number * (10**(-decimal)))
            decimal += 1

def decimalPoint( ):
    global decimal
    if (decimal == 0):
        decimal = 1

def exponent( ):
    global exp
    exp = True
    
def complexN( ):
    global decimal, compl
    compl = True
    decimal = 0

def clear( ):
    global num, num1, compl, decimal
    num = 0
    num1 = 0
    decimal = 0
    compl = False

"""
Given a number pressed, call the appropriate
function.
"""
def interpretPress( key ):
    if (key == "A"):
        #exponent()
        print("A")
    if (key == "B"):
        #complexN()
        print("B")
    if (key == "C"):
        print("C")
    if (key == "D"):
        print("D")
    if (key == "E"):
        print("E")
    if (key == "F"):
        print("F")
    if (key == "G"):
        print("G")
    if (key == "H"):
        print("H")
    if (key == "I"):
        print("I")
    if (key == "J"):
        print("J")
    if (key == "K"):
        print("K")
    if (key == "L"):
        print("L")
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
    #```````````````````````````````````````````````````````````````````````````````gggggggggggggggggggg print("\n" + str(num))
    
    while(True):
        
        # Scan buttons/keypad
        key = getKey(col_list, row_list)
        
        # A new key is pressed
        if key != None and key != lastKey:
            interpretPress(key)
            #if (num1 == 0):
            #    print()#hprint("\n" + str(num))
            #else:
            #    print("\n" + str(num) + " + j" + str(num1))
            lastKey = key
            
        # A key was released
        elif key == None:
            lastKey = None
        
        sleep(0.3)
        
    
        

if __name__ == "__main__":
    main()


