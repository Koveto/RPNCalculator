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

DIGITS_ON_SCREEN = 19
ORANGE = False

textY = "Y: 0.0000"
textX = "X: 0.0000"
numY = 0.0000
numX = 0.0000

stack = []

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


"""
Return 0 if stack is empty. Return top of the stack. 
"""
def peek():
    if stack == []:
        return 0
    else:
        return stack[len(stack) - 1]
    
"""
Return 0 if stack is empty. Remove item from the top of
the stack and return it. 
"""
def pop():
    if stack == []:
        return 0
    else:
        return stack.pop()

"""
Add zeros to the end of the text so there are at least four decimal places. 
"""
def appendZeros(text):
    if len(text) < 4 and "." not in text:
        text += "." + ("0" * (5 - len(text)))
    elif len(text) < 4:
        text += "0" * (5 - len(text))
    return text

"""
Takes boolean, True for X and False for Y. Returns output
to be displayed on X or Y in the form "X: {number}_" where
number is numX or numY. If the number is too long, "X. "
is replaced with "…" and the number is cropped. 
"""
def formatNumber( isX ):
    if isX:
        numXOrY = numX
        display = "X: " + str(numXOrY) + "_"
    else:
        numXOrY = numY
        display = "Y: " + str(numXOrY) + "_"
    if len(display) > 3 + DIGITS_ON_SCREEN:
        return "..." + str(numXOrY)[len(str(numXOrY)) - DIGITS_ON_SCREEN:] + "_"
    return display

"""
Takes a single number 0-9. Where no underscore is
displayed, it starts a new number. Otherwise, it
determines how much to add to the existing number
depending on the decimal place. It updates the display
and calls formatNumber(True). Calls peek() to put the
top of the stack in Y. 
"""
def numberPressed( digit ):
    global numX, textX, textY

    # A number is already in progress...
    if "_" in textX:

        # "X: 1_" -> "X: 1"
        sub = textX[:len(textX) - 1]

        # Decimal found! Figure out how much to add
        if ("." in str(numX) or sub[len(sub) - 1] == "."):
            if sub[len(sub) - 1] == ".":
                begin = len(textX)
            else:
                begin = str(numX).index(".")
            end = len(str(numX)) - 1
            dif = end - begin
            numX += float("0." + (dif * "0") + str(digit))

        # No decimal. Multiply by ten and add new digit
        else:
            numX = int((numX * float(10)) + float(str(digit)))

        # Update display
        textX = formatNumber(True)

    # New number
    else:
        number = str(float(peek()))
        number = appendZeros(number)
        textY = "Y: " + number
        numX = int(str(digit))
        textX = formatNumber(True)

"""
"Enter" button. Adds the existing number to the top (end)
of stack twice. Updates display so X and Y show the top
two numbers (which are the same) on the stack. Calls
appendZeros(number) to format the number. 
"""
def enter():
    global stack, textX, textY, numX
    stack = stack + [numX]
    stack = stack + [numX]
    number = str(peek())
    number = appendZeros(number)
    textY = "Y: " + number[:DIGITS_ON_SCREEN + 1]
    textX = "X: " + number[:DIGITS_ON_SCREEN + 1]

"""
"Backspace"/"Clear" button. If ORANGE, the stack is emptied.
Backspace clears the X register if a number isn't in progress
Where n is the digit being removed, 
X = (X – n) / 10 
if no decimal exists. If a decimal exists, let d be the distance
between the decimal place and n. Then,
X = X - (n * 10^(-1 * d))
Displays the new number on screen. Handles screen wrapping for
numbers beyond DIGITS_ON_SCREEN. 
"""
def backspaceClear():
    global numX, stack, ORANGE, textX, textY

    if ORANGE:
        stack = []
        textX = "X: 0.0000"
        textY = "Y: 0.0000"
        ORANGE = not ORANGE
        return
    
    if "_" in textX:
        digit = str(numX)[len(str(numX)) - 1]
        if "." in str(numX):
            if str(numX)[len(str(numX)) - 1] == ".":
                begin = len(textX)
            else:
                begin = str(numX).index(".")
            end = len(str(numX)) - 1
            dif = end - begin
            temp = 1 * (10 ** -1 * dif)
            # I get errors here. Backspace after 123456
            temp = float(digit) * float(temp)
            numX = numX - temp
            numX = str(numX).rstrip("0")
        else:
            numX = numX - int(digit) / 10

        if ("..." not in textX):
            textX = textX[:len(textX) - 2] + "_"
        else:
            t = textX[3:]
            n = str(numX)[:len(str(numX)) - DIGITS_ON_SCREEN]
            if len(n) == 0:
                textX = "X: " + str(numX) + "_"
            else:
                if "." not in n and "." not in t:
                    t = "." + t
                else:
                    t = n[len(n) - 1] + t
                if (t[:len(t) - 2] == str(numX)):
                    textX = "X: " + t[:len(t) - 2] + "_"
                else:
                    textX = "..." + t[:len(t) - 2] + "_"
    else:
        pop()
        numX = 0
        textX = "X: 0.0000"
        
"""
Decimal button. Does nothing if a number is being input and already
has a decimal place. Starts a new number at "0._" if no number is
being input. Otherwise, adds "._" to the display and scrolls if
necessary. 
"""
def decimalPoint():
    global numX, textX

    # Can't have decimals in decimals!
    if "." in str(numX) and "_" in textX:
        return
    
    # A number is already in progress...
    if "_" in textX:
        sub = textX[:len(textX) - 1]
        # Scroll the display if needed
        if len(textX) < DIGITS_ON_SCREEN - 3:
            textX = sub + "._"
        else:
            textX = "..." + sub[4:] + "._"

    # No number in progress. Start new!
    else:  
        textX = "X: 0._"
        numX = 0.0
        
"""
Calls enter() and pop() to add the current number (if any) once
to the stack. Calculates
number = (-1 * firstPop) + secondPop()
Calls pushOperation(number) to update the stack and display. 
"""
def addition(Z):
    global stack
    if "_" in textX:
        enter()
        pop()
    number = (Z * pop()) +  pop()
    pushOperation(number)


"""
Update Y and X using peek(), trimming the number, and appendZeros().
Add the number to the top of the stack. 
"""
def pushOperation(number):
    global stack, textX, textY
    temp = str(peek())
    if len(temp) > 19:
        temp = temp[:19]
    temp = appendZeros(temp)
    textY = "Y: " + temp
    temp = str(number)
    if len(temp) > 19:
        temp = temp[:19]
    temp = appendZeros(temp)
    textX = "X: " + temp
    stack = stack + [number]

"""
Given a number pressed, call the appropriate
function.
"""
def interpretPress( key ):
    if (key == "A"):
        decimalPoint()
    if (key == "B"):
        addition(1)
    if (key == "C"):
        addition(-1)
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
        backspaceClear()
    if (key == "0"):
        numberPressed(0)
    if (key == "#"):
        enter()
    

"""
Print the key pressed to the terminal
"""
def main():
    
    # Keep track of the last key
    lastKey = None
    
    # Display
    print("\n" + textY + "\n" + textX)
    
    while(True):
        
        # Scan buttons/keypad
        key = getKey(col_list, row_list)
        
        # A new key is pressed
        if key != None and key != lastKey:
            interpretPress(key)
            print("\n" + textY + "\n" + textX)
            lastKey = key
            
        # A key was released
        elif key == None:
            lastKey = None
        
        sleep(0.3)
        
    
        

if __name__ == "__main__":
    main()

