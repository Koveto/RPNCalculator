"""
pushButtons
12/19/2024 Kobe Goodwin

Given a list of pin numbers, create list
of Pin objects.
"""

from machine import Pin
from time import sleep

class PushButtons:
    
    def __init__(self, rowPinNos, colPinNos, buttonList):
        self.row_list = [None] * len(rowPinNos)
        self.col_list = [None] * len(colPinNos)
        self.key_list = buttonList

        # GP0-3 are output rows set to 1
        for x in range(0, len(rowPinNos)):
            self.row_list[x] = Pin(rowPinNos[x], Pin.OUT)
            self.row_list[x].value(1)

        # GP4-6 are input columns
        for x in range(0 ,len(colPinNos)):
            self.col_list[x] = Pin(colPinNos[x], Pin.IN, Pin.PULL_UP)
            
    """
    Scan the button array. Get the button pressed.
    """
    def getButton(self):
        row = self.row_list
        col = self.col_list
        # col Input Pins
        # row Output Pins
        for r in row:
            # iteration rows: 011111,101111,110111...
            r.value(0)
            # scan columns
            result = []
            for x in range(0, len(col)):
                result = result + [col[x].value()]
            # Where no button is pressed, [1,1,1,1,1,1]
            if min(result) == 0:
                # One of the buttons is pressed! One column is 0
                # Example: Pressing "B01"... result = [0,1,1,1,1,1]
                button = self.key_list[int(row.index(r))][int(result.index(0))]
                r.value(1)
                return (button)
            # Reset output to 1111
            r.value(1)
            
            
class PushButtonsDirect:
    
    def __init__(self,pins):
        self.buttons = [None] * len(pins)
        i = 0
        for pin in pins:
            self.buttons[i] = Pin(pin, Pin.IN, Pin.PULL_UP)
            i = i + 1

    def getButton(self):
        i = 0
        for button in self.buttons:
            if (button.value() == 0):
                sleep(0.05)
                if (button.value() == 0):
                    return i
            i = i + 1