"""
pushButtons
12/19/2024 Kobe Goodwin

Given a list of pin numbers, create list
of Pin objects.
"""

from machine import Pin

class pushButtonList:
    def __init__(self, pins):
        self.buttons = [None] * len(pins)
        i = 0
        for pin in pins:
            self.buttons[i] = [Pin(pin, Pin.IN, Pin.PULL_UP)]
            i = i + 1

    def getKey():
        global buttons
        i = 0
        for button in buttons:
            if (button.value() == 0):
                sleep(0.05)
                if (button.value() == 0):
                    return i
            i = i + 1