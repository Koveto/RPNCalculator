"""
calculator.py
10/29/2024 Kobe Goodwin

Reverse Polish Notation (RPN) Calculator
Raspberry-Pi Pico program

GP0-6 -> 4x3 Keypad (0 to leftmost i/o)
GP16-19 -> K4-K1
GP20-22 -> Breadboard E-G
GP26-28 -> Breadboard H-J
GP14-15 -> Breadboard L-K
Power and ground the breadboard
"""

from machine import Pin
from time import sleep
import cmath

numReal = 0   # real
numImag = 0  # imag

stackReal = []
stackImag = []

decimal = 0
compl = False
isPolar = False

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
    global numReal, numImag, decimal, comp
    if decimal == 0:
        if not compl:
            numReal = 10*numReal + number
        else:
            numImag = 10*numImag + number
    else:
        if not compl:
            numReal = numReal + (number * (10**(-decimal)))
        else:
            numImag = numImag + (number * (10**(-decimal)))
        decimal += 1

def add( negative ):
    global numReal, numImag
    n = pop()
    nReal = n[0]
    nImag = n[1]
    y = 1j*(nImag) + nReal
    z = 1j*(numImag) + numReal
    if negative:
        a = y - z
    else:
        a = y + z
    numReal = a.real
    numImag = a.imag
    
def multiply( ):
    global numReal, numImag
    n = pop()
    nReal = n[0]
    nImag = n[1]
    y = 1j*(nImag) + nReal
    z = 1j*(numImag) + numReal
    a = y * z
    numReal = a.real
    numImag = a.imag

def divide( ):
    global numReal, numImag
    if (numReal == 0 and numImag == 0):
        return
    n = pop()
    nReal = n[0]
    nImag = n[1]
    y = 1j*(nImag) + nReal
    z = 1j*(numImag) + numReal
    a = y / z
    numReal = a.real
    numImag = a.imag
    
def power( ):
    global numReal, numImag
    n = pop()
    nReal = n[0]
    nImag = n[1]
    y = 1j*(nImag) + nReal
    z = 1j*(numImag) + numReal
    #print(str(y) + "," + str(z))
    a = y ** z
    numReal = a.real
    numImag = a.imag
    
def invert( ):
    global numReal, numImag
    if (numReal == 0 and numImag == 0):
        return
    y = 1j*(numImag) + numReal
    a = 1 / y
    numReal = a.real
    numImag = a.imag
    
def negative( ):
    global numReal, numImag
    y = 1j*(numImag) + numReal
    a = y * -1
    numReal = a.real
    numImag = a.imag

def decimalPoint( ):
    global decimal
    if (decimal == 0):
        decimal = 1

def exponent( ):
    global numReal, numImag
    n = pop()
    nReal = n[0]
    nImag = n[1]
    y = 1j*(nImag) + nReal
    z = 1j*(numImag) + numReal
    #r = 
    #theta = cmath.phase(z)
    a = y * (10 ** z)
    numReal = a.real
    numImag = a.imag
    
def polar( ):
    global isPolar
    isPolar = not isPolar
    
def complexN( ):
    global decimal, compl
    compl = not compl
    decimal = 0

def push( ):
    global stackReal, stackImag, numReal, numImag, decimal, compl
    stackReal = stackReal + [numReal]
    stackImag = stackImag + [numImag]
    numReal = 0
    numImag = 0
    decimal = 0
    compl = False
    
def pop( ):
    global stackReal, stackImag
    if (len(stackReal) == 0):
        return [0, 0]
    r = stackReal[-1]
    i = stackImag[-1]
    del stackReal[-1]
    del stackImag[-1]
    return [r, i]

def peek( ):
    return [stackReal[-1], stackImag[-1]]

def back( ):
    global numReal, numImag, compl, decimal
    if (compl == True and decimal == 0):
        numImag = int(numImag) // 10
    if (compl == False and decimal == 0):
        numReal = int(numReal) // 10
    else:
        numReal = 0
        numImag = 0
        decimal = 0
        compl = False

def clear( ):
    global numReal, numImag, stackReal, stackImag, compl, decimal
    numReal = 0
    numImag = 0
    decimal = 0
    stackReal = []
    stackImag = []
    compl = False
    
def display( ):
    #print("D:" + str(numImag))
    if (len(stackReal) == 0):
        print("\n0")
    else:
        if (stackImag[-1] == 0):
            print("\n" + str(stackReal[-1]))
        else:
            if isPolar:
                z = stackReal[-1] + 1j*(stackImag[-1])
                a = cmath.sqrt((z.real ** 2) + (z.imag ** 2)).real
                b = cmath.phase(z)
            else:
                a = stackReal[-1]
                b = stackImag[-1]
            if (str(b)[0] != "-"):
                neg = "+"
                nm = 1
            else:
                neg = "-"
                nm = -1
            print("\n" + str(a) + " " + neg + " j" + str(b*nm))
    if (decimal == 1):
        dec = "."
    else:
        dec = ""
    if (numImag == 0 and compl == False):
        print(str(numReal) + dec)
    else:
        if isPolar:
            z = numReal + 1j*(numImag)
            a = cmath.sqrt((z.real ** 2) + (z.imag ** 2)).real
            b = cmath.phase(z)
        else:
            a = numReal
            b = numImag
        if (str(b)[0] != "-"):
            neg = "+"
            nm = 1
        else:
            neg = "-"
            nm = -1
        if (compl == False):
            print(str(a) + dec + " " + neg + " j" + str(b*nm))
        else:
            print(str(a) + " " + neg + " j" + str(b*nm) + dec)

"""
Given a number pressed, call the appropriate
function.
"""
def interpretPress( key ):
    if (key == "A"):
        exponent()
        #print("A")
    if (key == "B"):
        complexN()
        #print("B")
    if (key == "C"):
        push()
        #print("C")
    if (key == "D"):
        decimalPoint()
        #print("D")
    if (key == "E"):
        add(False)
        #print("E")
    if (key == "F"):
        add(True)
        #print("F")
    if (key == "G"):
        multiply()
        #print("G")
    if (key == "H"):
        divide()
        #print("H")
    if (key == "I"):
        power()
        #print("I")
    if (key == "J"):
        polar()
        #print("J")
    if (key == "K"):
        invert()
        #print("K")
    if (key == "L"):
        negative()
        #print("L")
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
        back()
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
    print("0\n0")
    
    while(True):
        
        # Scan buttons/keypad
        key = getKey(col_list, row_list)
        
        # A new key is pressed
        if key != None and key != lastKey:
            interpretPress(key)
            display()
            lastKey = key
            
        # A key was released
        elif key == None:
            lastKey = None
        
        sleep(0.3)
        
    
        

if __name__ == "__main__":
    main()


