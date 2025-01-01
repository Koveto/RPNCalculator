"""
display.py
12/30/2024
Determine what to display to the LCD
"""

from stack import Stack
from number import Number

X_ON = "X: "
X_OFF = "..."
Y = "Y: "

class Display:
    def __init__(self, ROWS, COLUMNS):
        self.rows = ROWS
        self.cols = COLUMNS
        self.x = "0.0000"
        self.numX = Number(0)
        self.y = "0.0000"
        self.numY = Number(0)
        self.isOffScreen = False
        self.isTyping = False
        self.stack = Stack()
        
    def get( self ):
        if (self.isOffScreen):
            pre = X_OFF
        else:
            pre = X_ON
        if (self.isTyping):
            post = "_"
        else:
            post = ""
        return (pre + self.x + post, Y + self.y)
    
    def __strNumber( self, number ):
        s = str(number)
        return s
    
    """
    Takes a single number 0-9. Where no underscore is
    displayed, it starts a new number. Otherwise, it
    determines how much to add to the existing number
    depending on the decimal place. It updates the display
    and calls formatNumber(True). Calls peek() to put the
    top of the stack in Y. 
    """
    """def numberPressed(digit):
        # A number is already in progress...
        if isTyping:

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
            #if (len(self.stack) != 0):
            self.numX = Number(digit)
            number = str(Decimal(peek()))
            number = appendZeros(number)
            setTextY("Y: " + number)
            numX = Decimal(str(digit))
            setTextX(formatNumber(True))
        """
