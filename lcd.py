"""
lcd.py
2/11/2025 Kobe Goodwin

Manipulate the LCD screen

write_at(x, y, string)
x: x cursor position
y: y cursor position
string: String containing message
write string starting at x,y. Wraps around

init(col, row, SDA, SCL)
col: number of columns for the LCD
row: number of rows for the LCD
SDA: number of the pin used for serial data
SCL: number of the pin used for serial clock
"""

from machine import Pin, SoftI2C
from lcd_i2c import I2cLcd

class Lcd:
    def __init__(self, col, row, SDA, SCL):
        self.address = 39
        self.i2c = SoftI2C(sda=Pin(SDA), scl=Pin(SCL), freq=400000)
        self.lcd = I2cLcd(self.i2c, self.address, row, col)
   
    def write_at(self,x,y,string):
        self.lcd.move_to(x,y)
        self.lcd.putstr(string)

"""class Lcd_Parallel:
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
       
    def write_at(self,x,y,string):
        self.move_cursor(x,y)
        self.write(string)
"""
