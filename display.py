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
        self.x = ""
        self.y = None
        self.isOffScreen = False
        self.isTyping = False
        self.stack = Stack()
        
    def get( self ):
        if (self.isTyping):
            
            if (len(self.x) == self.cols - 3):
                self.isOffScreen = True
                strX = self.x[1:]
            elif (len(self.x) > self.cols - 3):
                strX = self.x[len(self.x) - self.cols + 4:]
            else:
                strX = self.x
                self.isOffScreen = False
                
        else:
            
            strX = self.__abbreviate(self.x)
            self.isOffScreen = False
            
        strY = self.__abbreviate(str(self.y))
        if (strY == "" or self.y == None or strY == "None"):
            strY = "0"
            
        if (self.isOffScreen):
            pre = X_OFF
        else:
            pre = X_ON
        if (self.isTyping):
            post = "_"
        else:
            post = ""
        tempX = pre + strX + post
        tempY = Y + strY
        finalX = tempX + ((COLUMNS-len(tempX))*" ")
        finalY = tempY + ((COLUMNS-len(tempY))*" ")
            
        return (finalX, finalY)
    
    def clear( self ):
        self.stack = Stack()
        self.x = "0"
        self.y = 0
        self.isOffScreen = False
        self.isTyping = False
    
    def numberPressed( self, digit ):
        if (self.isTyping):
            if (len(self.x) > 99):
                return
            self.x += str(digit)
        else:
            self.stack.push(self.__getXNumber())
            self.y = self.stack.peek()
            self.x = str(digit)
            self.isTyping = True
    
    def backspace( self ):
        if (not self.isTyping):
            self.stack.pop()
            self.numberPressed(0)
            #self.isTyping = True
            return
        if (len(self.x) == 1):
            self.x = "0"
            self.isTyping = False
            return
        self.x = self.x[:len(self.x) - 1]
    
    def enter( self ):
        n = self.__getXNumber()
        self.stack.push(n)
        self.y = self.stack.peek()
        self.isTyping = False
        
    def add( self ):
        n1 = self.__getXNumber()
        n2 = self.stack.pop()
        if (n2 == None):
            n2 = Number(0)
        n3 = n1 + n2
        self.y = self.stack.peek()
        self.x = str(n3)
        self.isTyping = False
        self.isOffScreen = False
        
    def sub( self ):
        n1 = self.__getXNumber()
        n2 = self.stack.pop()
        if (n2 == None):
            n2 = Number(0)
        n3 = n2 - n1
        self.y = self.stack.peek()
        self.x = str(n3)
        self.isTyping = False
        self.isOffScreen = False
        
    def mul( self ):
        n1 = self.__getXNumber()
        n2 = self.stack.pop()
        if (n2 == None):
            n2 = 0
        n3 = n1 * n2
        self.y = self.stack.peek()
        self.x = str(n3)
        self.isTyping = False
        self.isOffScreen = False
        
    def div( self ):
        n1 = self.__getXNumber()
        n2 = self.stack.pop()
        if (n2 == None):
            n2 = 0
        n3 = n2 / n1
        self.y = self.stack.peek()
        self.x = str(n3)
        self.isTyping = False
        self.isOffScreen = False
        
    def __abbreviate( self, s ):
        if (len(s) < self.cols - 3):
            return s
        return s[0] + "." + s[1:3] + "E+" + str(len(s) - 1)
    
    def __getXNumber( self ):
        if ("." not in self.x and self.x != ""):
            return int(self.x)
        return 0
    
        # 55555555555555555555
        # 5.5555E+15
        # 5.5555E+19
