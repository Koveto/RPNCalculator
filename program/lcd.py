"""
lcd.py
5/7/2025

Self-contained module for manipulating an LCD screen.
Our PCB has 6 GPIO pin connections to the LCD:
 RS EN D4 D5 D6 D7
We used 4-bit parallel communication protocol.
 0000 = D7 D6 D5 D4
"""

from machine import Pin
from time import sleep_ms, sleep_us

ROWS = 4
COLUMNS = 20

class LCD:
    def __init__(self, rs_pin, enable_pin, d4_pin, d5_pin, d6_pin, d7_pin):
        """
        Initializes the LCD display.

        Args:
            rs_pin     (int): Pin number used for RS.
            enable_pin (int): Pin number used for enable.
            d4_pin     (int): Pin number used for D4
            d5_pin     (int): Pin number used for D5
            d6_pin     (int): Pin number used for D6
            d7_pin     (int): Pin number used for D7
        
        Returns:
            Instance of LCD
        """
        self._rs_pin = Pin(rs_pin, Pin.OUT)
        self._enable_pin = Pin(enable_pin, Pin.OUT)
        self._d4_pin = Pin(d4_pin, Pin.OUT)
        self._d5_pin = Pin(d5_pin, Pin.OUT)
        self._d6_pin = Pin(d6_pin, Pin.OUT)
        self._d7_pin = Pin(d7_pin, Pin.OUT)
        self._rs_pin.value(0)
        self._enable_pin.value(0)
        self._d4_pin.value(0)
        self._d5_pin.value(0)
        self._d6_pin.value(0)
        self._d7_pin.value(0)
        sleep_ms(20)
        self._write_4bits(0b0011) # d7654
        sleep_ms(5)    # > 4.1 ms
        self._write_4bits(0b0011)
        sleep_ms(1)
        self._write_4bits(0b0011)
        sleep_ms(1)
        self._write_4bits(0b0010)
        sleep_ms(1)
        self.rows = ROWS
        self.columns = COLUMNS
        self._cursor_x = 0
        self._cursor_y = 0
        self._backlight = True
        self._write_8bits(0b0000_1000) # display off
        self.clear()
        self._write_8bits(0b0000_0110)
        self._write_8bits(0b0000_1100) # hide cursor
        self._write_8bits(0b0000_1100) # display on
        self._write_8bits(0b0010_1000)

    def clear(self):
        """
        Clears the LCD display.
        
        Returns:
            None
        """
        self._rs_pin.value(0)
        self._write_8bits(0b0000_0001)
        sleep_ms(5)
        self._write_8bits(0b0000_0010)
        sleep_ms(5)
        self._cursor_x = 0
        self._cursor_y = 0
        
    def move_to(self, x, y):
        """
        Moves cursor to (x, y)
        
        Args:
            x (int): x position
            y (int): y position
        
        Returns:
            None
        """
        self._rs_pin.value(0)                # Ex. (1, 3)
        addr = self._cursor_x & 0x3f         # 0000_0001 & 0011_1111 = 0000_0001
        if self._cursor_y & 1:               # 0000_0011 & 0000_0001 = 0000_0001 True!
            addr += 0x40                     # 0000_0001 + 0100_0000 = 0100_0001
        if self._cursor_y & 2:               # 0000_0011 & 0000_0010 = 0000_0010 True!
            addr += self.columns             # 0100_0001 + 0001_0100 = 0101_0101
        addr |= 0x80                         # 0101_0101 | 1000_0000 = 1101_0101
        self._write_8bits(addr)
        if (addr) <= 3:
            sleep_ms(5)
        
    def write(self, string):
        """
        Writes a string at the cursor position on the LCD display.
        
        Args:
            string (str): String containing the message to display.
            
        Returns:
            None
        """    
        for char in string:
            self._rs_pin.value(1)
            char = ord(char) # "X" = 88 = 0101_1000
            self._write_8bits(char)
            self._cursor_x += 1
            if self._cursor_x >= self.columns:
                self._cursor_x = 0
                self._cursor_y += 1
            if self._cursor_y >= self.rows:
                self._cursor_y = 0
            self.move_to(self._cursor_x, self._cursor_y)

    def write_at(self, x, y, string):
        """
        Writes a string at the specified (x, y) position on the LCD display.

        Args:
            x      (int): X cursor position.
            y      (int): Y cursor position.
            string (str): String containing the message to display.
            
        Returns:
            None
        """
        self._cursor_x = x
        self._cursor_y = y
        self.move_to(self._cursor_x, self._cursor_y)
        self.write(string)
                
    def custom_char(self, location, charmap):
        """
        Write a character to one of the 8 CGRAM locations, available
        as chr(0) through chr(7).
        See https://maxpromer.github.io/LCD-Character-Creator/
        
        8 rows, 5 columns.
        Each number represents a row.
        First number is top row.
        Each bit fills in row, column position.
        Ex. 0x13 X--XX
        
        Example usage:
        custom_char(0, bytearray([0x00, 0x01, 0x03, 0x06, 0x0C, 0x18, 0x1F, 0x00]))
        write(chr(0))
        
        Args:
            location      (int): Index of chr to replace
                                 Valid 0-7
            charmap (bytearray): bytearray of row list
        
        Returns:
            None
        """
        location &= 0x7
        cmd = 0x40 | (location << 3)
        self._rs_pin.value(0)
        self._write_8bits(cmd)
        sleep_us(40)
        for i in range(8):
            self._rs_pin.value(1)
            self._write_8bits(charmap[i])
            sleep_us(40)
        self.move_to(self._cursor_x, self._cursor_y)
        
    def _write_8bits(self, bits):
        """
        Writes 8 bits. Upper 4, then lower 4.
        
        Args:
            bits (int): bits to write
        
        Returns:
            None
        """
        self._write_4bits(bits >> 4)
        self._write_4bits(bits)
    
    def _write_4bits(self, bits):
        """
        Writes 4 bits to D7,D6,D5,D4.
        
        Args:
            bits (int): bits to write
        
        Returns:
            None
        """
        self._d7_pin.value(bits & 0x08)
        self._d6_pin.value(bits & 0x04)
        self._d5_pin.value(bits & 0x02)
        self._d4_pin.value(bits & 0x01)
        self._enable_pin.value(0)
        sleep_us(1)
        self._enable_pin.value(1)
        sleep_us(1)       # > 450 ns
        self._enable_pin.value(0)
        sleep_us(100)     # > 37 us
        




