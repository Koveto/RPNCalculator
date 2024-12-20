"""
keypad.py
12/19/2024 Kobe Goodwin

getKey()
Scan the keypad. Return a key if pressed.

newKeypad(R1, R2, R3, R4, C1, C2, C3)
Given pin assignments, make 3 lists.
row_list... Output pins, 4 rows
col_list... Input pins, 3 columns
key_list... Characters found at the locations
"""

from machine import Pin

class keypadInput:
    def __init__(self, R1, R2, R3, R4, C1, C2, C3):
        self.row_list = [R1, R2, R3, R4]  
        self.col_list = [C1, C2, C3]

        # GP0-3 are output rows set to 1
        for x in range(0, 4):
            self.row_list[x] = Pin(self.row_list[x], Pin.OUT)
            self.row_list[x].value(1)

        # GP4-6 are input columns
        for x in range(0 ,3):
            self.col_list[x] = Pin(self.col_list[x], Pin.IN, Pin.PULL_UP)

        self.key_list = [["1", "2", "3"],\
                        ["4", "5", "6"],\
                        ["7", "8", "9"],\
                        ["*", "0", "#"]]

    def getKey():
        # col = [GP4, GP5, GP6] Input Pins
        # row = [GP0, GP1, GP2, GP3] Output Pins
        # r = GP0, GP1, GP2, GP3
        for r in row_list:
            # iteration GP0-3 rows: 0111,1011,1101,1110
            r.value(0)
            # scan GP4-6 columns
            result = [col_list[0].value(), col_list[1].value(), col_list[2].value()]
            # Where no button is pressed, [1,1,1]
            if min(result) == 0:
                # One of the buttons is pressed! One column is 0
                # Example: Pressing "1"... result = [0,1,1]
                # key = key_list[ [GP0, GP1, GP2, GP3].index(GP0)][ [0,1,1].index(0) ]
                # key =	key_list[0][0] = 1
                key = key_list[int(row_list.index(r))][int(result.index(0))]
                r.value(1)
                return (key)
            # Reset output to 1111
            r.value(1)

