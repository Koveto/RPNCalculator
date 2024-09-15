"""

Reverse Polish Notation (RPN) Calculator

Contributors:
Kale Erickson
Kobe Goodwin
Gabe Wichmann

SD_403_05
09/14/2024

"""

# Window application for proof-of-concept
import tkinter as tk
from PIL import ImageTk, Image
import os

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
textY = canvas.create_text(130,140,text="Y: 0.0000", font="terminal 19 bold", fill = "black")
textX = canvas.create_text(130,170,text="X: 0.0000", font="terminal 19 bold", fill = "black")

# Main program
def main():
    # Click activates function
    canvas.bind("<Button-1>", click)

    # Run window
    root.mainloop()

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
    print("Button 13 pressed")

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
    print("Button 17 pressed")

# Up
def button18():
    print("Button 18 pressed")

# 7
def button19():
    print("Button 19 pressed")

# 8
def button20():
    print("Button 20 pressed")

# 9
def button21():
    print("Button 21 pressed")

# Divison
def button22():
    print("Button 22 pressed")

# Down
def button23():
    print("Button 23 pressed")

# 4
def button24():
    print("Button 24 pressed")

# 5
def button25():
    print("Button 25 pressed")

# 6
def button26():
    print("Button 26 pressed")

# Multiplication
def button27():
    print("Button 27 pressed")

# Orange
def button28():
    print("Button 28 pressed")

# 1
def button29():
    print("Button 29 pressed")

# 2
def button30():
    print("Button 30 pressed")

# 3
def button31():
    print("Button 31 pressed")

# Subtraction
def button32():
    print("Button 32 pressed")

# Exit
def button33():
    print("Button 33 pressed")

# 0
def button34():
    print("Button 34 pressed")

# .
def button35():
    print("Button 35 pressed")

# R/S
def button36():
    print("Button 36 pressed")

# Addition
def button37():
    print("Button 37 pressed")


# Change the upper text
def changeTextY(text):
    canvas.itemconfigure(textY,text=text)

# Change the lower text
def changeTextX(text):
    canvas.itemconfigure(textX,text=text)

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
            if i == 37: 
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