"""
display.py
2/11/2025
Determine what to display to the LCD

init(ROWS, COLUMNS)
ROWS: Number of rows on LCD
COLUMNS: Number of columns on LCD
Prepares a blank output to the LCD

get()
Returns (x, y) where...
x is x row to display
ex. "X: 0            "
y is y row to display
ex. "Y: 0            "

clear()
Reset X and Y to 0

numberPressed(digit)
Append the number to the X row

backspace()
Remove the last digit from the X row

enter()
Push the X row to the stack

add()
Add X and Y rows, output to X

sub()
Subtract Y-X rows, output to X

mul()
Multiply X and Y rows, output to X

div()
Divide Y/X rows, output to X

__abbreviate(s)
s: String representing some number
Return a shortened s using scientific notation

__getXNumber()
Convert x to a number and returns it
"""

from stack import Stack

# Constants
X_ON = "X: "
X_OFF = "..."
Y = "Y: "

class Display:
    def __init__(self, ROWS, COLUMNS):
        self.rows = ROWS
        self.cols = COLUMNS
        self.x = 0
        self.y = 0
        self.isOffScreen = False
        self.isTyping = False
        self.stack = Stack()
        
    def get( self ):
        return ("X: 0           ","Y: 0            ")
    
    def clear( self ):
        pass
    
    def numberPressed( self, digit ):
        pass
    
    def backspace( self ):
        pass
    
    def enter( self ):
        pass
        
    def add( self ):
        pass
        
    def sub( self ):
        pass
        
    def mul( self ):
        pass
        
    def div( self ):
        npass
        
    def __abbreviate( self, s ):
        pass
    
    def __getXNumber( self ):
        pass
