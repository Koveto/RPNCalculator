"""

Reverse Polish Notation (RPN) Calculator

Contributors:
Kale Erickson
Kobe Goodwin
Gabe Wichmann

SD_403_05
10/6/2024

"""

# Window application for proof-of-concept
import tkinter as tk
from PIL import ImageTk, Image
import os
from decimal import *

stack = []

numX = Decimal("0.0000")        # Number being stored in X
numY = Decimal("0.0000")        # Number being stored in Y

DIGITS_ON_SCREEN = 19

WIDTH = 338     # Width of screen
HEIGHT = 615    # Height of screen
#           Left, Right, Top, Bottom
BUTTON01 = (30,62,256,279)      # Sum
BUTTON02 = (79,114,258,281)     # Inverse
BUTTON03 = (130,164,258,280)    # Sqrt
BUTTON04 = (178,212,258,280)    # Log
BUTTON05 = (227,260,259,282)    # Ln
BUTTON06 = (276,311,257,283)    # Xeq
BUTTON07 = (29,65,307,334)      # Sto
BUTTON08 = (81,116,308,332)     # Rcl
BUTTON09 = (129,162,305,332)    # R
BUTTON10 = (178,213,304,331)    # Sin
BUTTON11 = (224,262,304,331)    # Cos
BUTTON12 = (276,311,305,330)    # Tan
BUTTON13 = (30,115,353,381)     # Enter
BUTTON14 = (129,165,353,377)    # Comparison
BUTTON15 = (177,214,351,378)    # Plus/Minus
BUTTON16 = (236,262,353,381)    # E
BUTTON17 = (277,311,354,380)    # Backspace
BUTTON18 = (30,63,399,428)      # Up
BUTTON19 = (87,131,398,429)     # 7
BUTTON20 = (145,191,401,430)    # 8
BUTTON21 = (205,251,402,431)    # 9
BUTTON22 = (266,312,400,429)    # Division
BUTTON23 = (31,67,452,478)      # Down
BUTTON24 = (86,132,447,478)     # 4
BUTTON25 = (146,191,448,478)    # 5
BUTTON26 = (206,250,450,478)    # 6
BUTTON27 = (263,311,449,476)    # Multiplication
BUTTON28 = (29,66,496,527)      # Orange
BUTTON29 = (86,132,496,526)     # 1
BUTTON30 = (147,192,498,526)    # 2
BUTTON31 = (206,252,496,525)    # 3
BUTTON32 = (265,312,496,525)    # Subtraction
BUTTON33 = (26,65,544,574)      # Exit
BUTTON34 = (86,133,544,573)     # 0
BUTTON35 = (145,193,544,573)    # .
BUTTON36 = (204,251,546,573)    # R/S
BUTTON37 = (264,311,541,572)    # Addition
BUTTONS = ( BUTTON01, BUTTON02, BUTTON03, BUTTON04, BUTTON05,
            BUTTON06, BUTTON07, BUTTON08, BUTTON09, BUTTON10,
            BUTTON11, BUTTON12, BUTTON13, BUTTON14, BUTTON15,
            BUTTON16, BUTTON17, BUTTON18, BUTTON19, BUTTON20,
            BUTTON21, BUTTON22, BUTTON23, BUTTON24, BUTTON25,
            BUTTON26, BUTTON27, BUTTON28, BUTTON29, BUTTON30,
            BUTTON31, BUTTON32, BUTTON33, BUTTON34, BUTTON35,
            BUTTON36, BUTTON37 )

# Create the window
root = tk.Tk()
root.title("RPN Calculator")
root.geometry(str(WIDTH) + "x" + str(HEIGHT))
root.resizable(False,False)

# Create the background
img = ImageTk.PhotoImage(Image.open("background.png"))
canvas = tk.Canvas(root, width = WIDTH, height = HEIGHT, highlightthickness=0)
canvas.pack()
canvas.create_image(WIDTH/2, HEIGHT/2, image=img)

# Create the text
textY = canvas.create_text(45,140,anchor="w",text="Y: 0.0000", font="terminal 17 bold", fill = "black")
textX = canvas.create_text(45,170,anchor="w",text="X: 0.0000", font="terminal 17 bold", fill = "black")

# Main program
def main():
    # Click activates function
    canvas.bind("<Button-1>", click)

    # Run window
    root.mainloop()

# Formats the X or Y lines around the current number
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
    
# Given a number pressed, update numX and display
def numberPressed(digit):
    global numX
    t = getTextX()

    # A number is already in progress...
    if "_" in t:

        # "X: 1_" -> "X: 1"
        sub = t[:len(t) - 1]

        # Decimal found! Figure out how much to add
        if ("." in str(numX) or sub[len(sub) - 1] == "."):
            if sub[len(sub) - 1] == ".":
                begin = len(t)
            else:
                begin = str(numX).index(".")
            end = len(str(numX)) - 1
            dif = end - begin
            numX += Decimal("0." + (dif * "0") + str(digit))

        # No decimal. Multiply by ten and add new digit
        else:
            numX = (numX * Decimal(10)) + Decimal(str(digit))

        # Update display
        setTextX(formatNumber(True))

    # New number
    else:
        number = str(Decimal(peek()))
        number = appendZeros(number)
        setTextY("Y: " + number)
        numX = Decimal(str(digit))
        setTextX(formatNumber(True))
        

# Sum
def button1():
    print("Button 1 pressed")

# Inverse
def button2():
    print("Button 2 pressed")

# Sqrt
def button3():
    print("Button 3 pressed")

# Log
def button4():
    print("Button 4 pressed")

# Ln
def button5():
    print("Button 5 pressed")

# Xeq
def button6():
    print("Button 6 pressed")

# Sto
def button7():
    print("Button 7 pressed")

# Rcl
def button8():
    print("Button 8 pressed")

# R
def button9():
    print("Button 9 pressed")

# Sin
def button10():
    print("Button 10 pressed")

# Cos
def button11():
    print("Button 11 pressed")

# Tan
def button12():
    print("Button 12 pressed")

# Enter
def button13():
    global stack
    global numX
    stack = stack + [numX]
    stack = stack + [numX]
    number = str(stack[len(stack) - 1])
    number = appendZeros(number)
    setTextY("Y: " + number[:DIGITS_ON_SCREEN + 1])
    setTextX("X: " + number[:DIGITS_ON_SCREEN + 1])

# Comparison
def button14():
    print("Button 14 pressed")

# Plus/Minus
def button15():
    print("Button 15 pressed")

# E
def button16():
    print("Button 16 pressed")

# Backspace
def button17():
    global numX
    if "_" in getTextX():
        digit = str(numX)[len(str(numX)) - 1]
        if "." in str(numX):
            if str(numX)[len(str(numX)) - 1] == ".":
                begin = len(getTextX())
            else:
                begin = str(numX).index(".")
            end = len(str(numX)) - 1
            dif = end - begin
            temp = Decimal(1) * (Decimal(10) ** (Decimal(-1) * Decimal(dif)))
            temp = Decimal(int(digit)) * Decimal(temp)
            numX = Decimal(numX) - Decimal(temp)
            numX = Decimal(str(numX).rstrip("0"))
        else:
            numX = Decimal(Decimal(Decimal(numX) - Decimal(int(digit))) / Decimal(10))

        if ("..." not in getTextX()):
            setTextX(getTextX()[:len(getTextX()) - 2] + "_")
        else:
            t = getTextX()[3:]
            n = str(numX)[:len(str(numX)) - DIGITS_ON_SCREEN]
            if len(n) == 0:
                setTextX("X: " + str(numX) + "_")
            else:
                if "." not in n and "." not in t:
                    t = "." + t
                else:
                    t = n[len(n) - 1] + t
                if (t[:len(t) - 2] == str(numX)):
                    setTextX("X: " + t[:len(t) - 2] + "_")
                else:
                    setTextX("..." + t[:len(t) - 2] + "_")
        
        print(getTextX())
        print("   " + str(numX))
        print()
    else:
        numX = 0
        setTextX("X: 0.0000")


# Up
def button18():
    print("Button 18 pressed")

# 7
def button19():
    numberPressed(7)

# 8
def button20():
    numberPressed(8)

# 9
def button21():
    numberPressed(9)

# Divison
def button22():
    global stack
    if "_" in getTextX():
        button13()
        pop()
    num1 = Decimal(pop())
    num2 = Decimal(pop())
    if num2 == 0:
        setTextY("Divide By Zero")
    else:
        number = num1 /  num2
        pushOperation(number)

# Down
def button23():
    print("Button 23 pressed")

# 4
def button24():
    numberPressed(4)

# 5
def button25():
    numberPressed(5)

# 6
def button26():
    numberPressed(6)

# Multiplication
def button27():
    global stack
    if "_" in getTextX():
        button13()
        pop()
    number = Decimal(pop()) *  Decimal(pop())
    pushOperation(number)

# Orange
def button28():
    print("Button 28 pressed")

# 1
def button29():
    numberPressed(1)

# 2
def button30():
    numberPressed(2)

# 3
def button31():
    numberPressed(3)

# Subtraction
def button32():
    addition(-1)

# Exit
def button33():
    print("Button 33 pressed")

# 0
def button34():
    numberPressed(0)

# .
def button35():
    global numX
    t = getTextX()

    # Can't have decimals in decimals!
    if "." in t and "_" in t:
        return
    
    # A number is already in progress...
    if "_" in t:
        sub = t[:len(t) - 1]
        # Scroll the display if needed
        if len(t) < 16:
            setTextX(sub + "._")
        else:
            setTextX(sub[1:] + "._")

    # No number in progress. Start new!
    else:
        setTextX("X: 0._")
        numX = Decimal(0.0)

# R/S
def button36():
    print("Button 36 pressed")

# Addition
def button37():
    addition(1)

# Add two numbers
def addition(MinusOneForSubtraction):
    global stack
    if "_" in getTextX():
        button13()
        pop()
    number = (Decimal(MinusOneForSubtraction) * Decimal(pop())) +  Decimal(pop())
    pushOperation(number)

# Get the number from the top of the stack
def peek():
    if stack == []:
        return 0
    else:
        return stack[len(stack) - 1]
    
# Get the number from the top of the stack and remove it
def pop():
    if stack == []:
        return 0
    else:
        return stack.pop()
    
# Append extra 0s to a number "3" -> "3.0000"
def appendZeros(text):
    if len(text) < 4 and "." not in text:
        text += "." + ("0" * (4 - len(text)))
    elif len(text) < 4:
        text += "0" * (4 - len(text))
    return text

# Change the upper text
def setTextY(text):
    canvas.itemconfigure(textY,text=text)

# Get the upper text
def getTextY():
    return canvas.itemcget(textY,'text')

# Change the lower text
def setTextX(text):
    canvas.itemconfigure(textX,text=text)

# Get the lower text
def getTextX():
    return canvas.itemcget(textX,'text')

# Put the top two numbers in stack to X and Y
def pushOperation(number):
    global stack
    temp = str(peek())
    if len(temp) > 19:
        temp = temp[:19]
    temp = appendZeros(temp)
    setTextY("Y: " + temp)
    temp = str(number)
    if len(temp) > 19:
        temp = temp[:19]
    temp = appendZeros(temp)
    setTextX("X: " + temp)
    stack = stack + [Decimal(number)]

# Called when the user clicks
def click(event):

    # Determine which button is being pressed, if any
    i = 0
    for button in BUTTONS:
        i += 1
        if (event.x > button[0] and event.x < button[1] and
            event.y > button[2] and event.y < button[3]):
            break
        else:
            if i == len(BUTTONS): 
                return
    
    # Call appropriate button function
    match (i):
        case 1:
            button1()
        case 2:
            button2()
        case 3:
            button3()
        case 4:
            button4()
        case 5:
            button5()
        case 6:
            button6()
        case 7:
            button7()
        case 8:
            button8()
        case 9:
            button9()
        case 10:
            button10()
        case 11:
            button11()
        case 12:
            button12()
        case 13:
            button13()
        case 14:
            button14()
        case 15:
            button15()
        case 16:
            button16()
        case 17:
            button17()
        case 18:
            button18()
        case 19:
            button19()
        case 20:
            button20()
        case 21:
            button21()
        case 22:
            button22()
        case 23:
            button23()
        case 24:
            button24()
        case 25:
            button25()
        case 26:
            button26()
        case 27:
            button27()
        case 28:
            button28()
        case 29:
            button29()
        case 30:
            button30()
        case 31:
            button31()
        case 32:
            button32()
        case 33:
            button33()
        case 34:
            button34()
        case 35:
            button35()
        case 36:
            button36()
        case 37:
            button37()

# Start program
if __name__ == "__main__":
    main()