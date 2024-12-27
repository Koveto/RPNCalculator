"""
display.py
12/26/2024
Determine what to display to the LCD
"""

X_ON = "X: "
X_OFF = "..."
Y = "Y: "

class Display:
    def __init__(self, ROWS, COLUMNS):
        self.rows = ROWS
        self.cols = COLUMNS
        self.x = "0.0000"
        self.y = "0.0000"
        self.offScreen = False
        
    def get( self ):
        if (self.offScreen):
            return (X_OFF + self.x, Y + self.y)
        return (X_ON + self.x, Y + self.y)
        