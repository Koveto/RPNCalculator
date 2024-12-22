"""
keypad.py
12/21/2024 Kobe Goodwin

Read input from a keypad
"""

from machine import Pin

class Keypad:
    def __init__(self, rowPinNos, colPinNos, keyList):
        self.row_list = [None] * len(rowPinNos)
        self.col_list = [None] * len(colPinNos)
        self.key_list = keyList

        # GP0-3 are output rows set to 1
        for x in range(0, len(rowPinNos)):
            self.row_list[x] = Pin(rowPinNos[x], Pin.OUT)
            self.row_list[x].value(1)

        # GP4-6 are input columns
        for x in range(0 ,len(colPinNos)):
            self.col_list[x] = Pin(colPinNos[x], Pin.IN, Pin.PULL_UP)

    def getKey(self):
        row = self.row_list
        col = self.col_list
        # col = [GP4, GP5, GP6] Input Pins
        # row = [GP0, GP1, GP2, GP3] Output Pins
        # r = GP0, GP1, GP2, GP3
        for r in row:
            # iteration GP0-3 rows: 0111,1011,1101,1110
            r.value(0)
            # scan GP4-6 columns
            result = []
            for x in range(0, len(col)):
                result = result + [col[x].value()]
            # Where no button is pressed, [1,1,1]
            if min(result) == 0:
                # One of the buttons is pressed! One column is 0
                # Example: Pressing "1"... result = [0,1,1]
                # key = key_list[ [GP0, GP1, GP2, GP3].index(GP0)][ [0,1,1].index(0) ]
                # key =	key_list[0][0] = 1
                key = self.key_list[int(row.index(r))][int(result.index(0))]
                r.value(1)
                return (key)
            # Reset output to 1111
            r.value(1)

