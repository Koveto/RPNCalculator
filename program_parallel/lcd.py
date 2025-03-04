"""
lcd.py
3/2/2025 Kobe Goodwin

Module for manipulating the LCD screen.
"""

from machine import Pin
from gpio_lcd import GpioLcd

class LCD:
    def __init__(self, row, col, RS, EN, D4, D5, D6, D7):
        """
        Initializes the LCD display.

        Args:
            col (int): Number of columns for the LCD.
            row (int): Number of rows for the LCD.
            RS (int): Pin number used for RS.
            EN (int): Pin number used for enable.
            D4 (int): Pin number used for D4
            D5 (int): Pin number used for D5
            D6 (int): Pin number used for D6
            D7 (int): Pin number used for D7
        """
        self.lcd = GpioLcd(RS, EN, D4, D5, D6, D7, row, col)
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

