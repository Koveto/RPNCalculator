"""
lcd.py
12/19/2024 Kobe Goodwin

Manipulate the LCD screen

cursor_at(x,y)
cursor goes to x,y

write(string)
write String string starting at x,y. Wraps around

newLCD(col, row, Rs, E, D4, D5, D6, D7)
-> return lcd (type:GpioLcd)
Create a gpio_lcd.GpioLcd object given the
number of rows, columns, and pins.

Code from https://www.circuitschools.com/interfacing-16x2-lcd-module-with-raspberry-pi-pico-with-and-without-i2c/
"""

from machine import Pin
from gpio_lcd import GpioLcd

class Lcd:
    def __init__(self, col, row, Rs, E, D4, D5, D6, D7):
        self.lcd = GpioLcd(rs_pin=Pin(Rs),
              enable_pin=Pin(E),
              d4_pin=Pin(D4),
              d5_pin=Pin(D5),
              d6_pin=Pin(D6),
              d7_pin=Pin(D7),
              num_lines=row, num_columns=col)
    
    def move_cursor(self,x, y):
        self.lcd.move_to(x,y)

    def write(self,string):
        self.lcd.putstr(string)

