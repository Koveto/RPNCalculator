"""
lcd.py
2/12/2025 Kobe Goodwin

Module for manipulating the LCD screen.
"""

from machine import Pin, SoftI2C
from lcd_i2c import I2cLcd

class LCD:
    def __init__(self, col, row, SDA, SCL, address=0x27):
        """
        Initializes the LCD display.

        Args:
            col (int): Number of columns for the LCD.
            row (int): Number of rows for the LCD.
            SDA (int): Pin number used for serial data.
            SCL (int): Pin number used for serial clock.
            address (int): I2C address for the LCD display (default is 0x27).
        """
        self.address = address
        self.i2c = SoftI2C(sda=Pin(SDA), scl=Pin(SCL), freq=400000)
        self.lcd = I2cLcd(self.i2c, self.address, row, col)
        self.rows = row
        self.columns = col
        self.clear()

    def clear(self):
        """Clears the LCD display."""
        self.lcd.clear()

    def write_at(self, x, y, string):
        """
        Writes a string at the specified (x, y) position on the LCD display.

        Args:
            x (int): X cursor position.
            y (int): Y cursor position.
            string (str): String containing the message to display.

        Raises:
            ValueError: If x or y is out of bounds for the LCD dimensions.
        """
        if not (0 <= x < self.columns and 0 <= y < self.rows):
            raise ValueError(f"Position ({x}, {y}) is out of bounds for the LCD dimensions.")

        self.lcd.move_to(x, y)
        self.lcd.putstr(string)

