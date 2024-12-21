"""
button_input.py
10/27/2024 Kobe Goodwin

Using edge interrupts, toggle 4 LEDs
depending on which button is pressed.
Handles debouncing by waiting 100 ms.

GP16-19 -> K1-4 
GP20-22 -> LED1-3
GP26 -> LED4
"""

from machine import Pin
from time import sleep

led1 = Pin(20, Pin.OUT)
led2 = Pin(21, Pin.OUT)
led3 = Pin(22, Pin.OUT)
led4 = Pin(26, Pin.OUT)

button1 = Pin(15, Pin.IN, Pin.PULL_UP)
def button1Pressed(button1):
    sleep(0.1)
    if (button1.value() == 0):
        led1.toggle()
button1.irq(trigger=Pin.IRQ_FALLING, handler=button1Pressed)

button2 = Pin(18, Pin.IN)
def button2Pressed(button2):
    sleep(0.1)
    if (button2.value() == 0):
        led2.toggle()
button2.irq(trigger=Pin.IRQ_FALLING, handler=button2Pressed)

button3 = Pin(17, Pin.IN)
def button3Pressed(button3):
    sleep(0.1)
    if (button3.value() == 0):
        led3.toggle()
button3.irq(trigger=Pin.IRQ_FALLING, handler=button3Pressed)

button4 = Pin(16, Pin.IN)
def button4Pressed(button4):
    sleep(0.1)
    if (button4.value() == 0):
        led4.toggle()
button4.irq(trigger=Pin.IRQ_FALLING, handler=button4Pressed)

def main():
    while(True):
        pass
        

if __name__ == "__main__":
    main()