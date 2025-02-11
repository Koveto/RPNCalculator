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
        self.xStr = "0"
        self.isOffScreen = False
        self.isTyping = False
        self.stack = Stack()
        
    def get( self ):
        xToReturn = X_ON + self.xStr + (" " * (len(X_ON + self.xStr)))
        yToReturn = Y + str(self.y) + (" " * (len(Y + str(self.y))))
        return (xToReturn,yToReturn)
    
    def clear( self ):
        self.x = 0
        self.y = 0
        self.stack = Stack()
    
    def numberPressed( self, digit ):
        if (self.isTyping):
            if (self.x.is_integer()):
                self.xStr += str(digit)
                self.x = (self.x * 10) + digit
            else:
                lastDigit = self.xStr[-1]
                
        else:
            self.__push()
            self.x = digit
            self.xStr = str(digit)
    
    def backspace( self ):
        if (not self.isTyping):
            self.x = 0
            self.xStr = "0"
            return
        self.x = self.x // 10
        self.xStr = self.xStr[:len(self.xStr)-1]
    
    def enter( self ):
        self.__push()
        self.x = 0
        self.xStr = "0"
        self.isTyping = False
        
    def add( self ):
        self.x = self.y + self.x
        self.__operation()
        
    def sub( self ):
        self.x = self.y - self.x
        self.__operation()
        
    def mul( self ):
        self.x = self.y * self.x
        self.__operation()
        
    def div( self ):
        if (self.x == 0):
            return
        self.x = self.y / self.x
        self.__operation()
        
    def __push( self ):
        self.stack.push(self.x)
        self.y = self.x
    
    def __operation( self ):
        self.stack.pop()
        if (self.stack.isEmpty()):
            self.y = 0
        else:
            self.y = stack.peek()
        self.xStr = str(self.x)
        self.isTyping = False
    
    def __abbreviate( self, s ):
        pass
    
    def __getXNumber( self ):
        pass

