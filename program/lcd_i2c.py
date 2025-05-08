"""
lcd.py
5/7/2025

Self-contained module for manipulating an LCD screen.
This code is used for communicating to an old PCB.
It uses I2C protocol, using a SDA and SCL pin.
This old PCB used a 16x2 LCD.
"""

from machine import Pin, SoftI2C, I2C
from utime import sleep_ms, sleep_us
import gc

ROWS = 2
COLUMNS = 16

class LCD_I2C:
    def __init__(self, sda_pin, scl_pin, address = 0x27):
        """
        Initializes the LCD display.

        Args:
            sda_pin (int): Pin number used for serial data.
            scl_pin (int): Pin number used for serial clock.
            address (int): I2C address
        
        Returns:
            Instance of LCD_I2C
        """
        self._i2c = SoftI2C(sda=Pin(sda_pin), scl=Pin(scl_pin), freq=400000)
        self._backlight = True
        self._i2c_addr = address
        self._i2c.writeto(self._i2c_addr, bytes([0]))
        sleep_ms(20)
        self._write_init_nibble(0x30)
        sleep_ms(5)
        self._write_init_nibble(0x30)
        sleep_ms(1)
        self._write_init_nibble(0x30)
        sleep_ms(1)
        self._write_init_nibble(0x20)
        sleep_ms(1)
        self._cursor_x = 0
        self._cursor_y = 0
        self._write_command(0x08)
        self._i2c.writeto(self._i2c_addr, bytes([1 << 3]))
        gc.collect()
        self.clear()
        self._write_command(0x06)
        self._write_command(0x0C)
        self._write_command(0x0C)
        self._write_command(0x28)
        gc.collect()
        self.rows = ROWS
        self.columns = COLUMNS
        self.clear()

    def clear(self):
        """
        Clears the LCD display.
        
        Returns:
            None
        """
        self._write_command(0x01)
        self._write_command(0x02)
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
        self._cursor_x = x
        self._cursor_y = y
        addr = x & 0x3f
        if y & 1:
            addr += 0x40 
        if y & 2:
            addr += self.columns
        self._write_command(0x80 | addr)
        
    def write(self, string):
        """
        Writes a string at the cursor position on the LCD display.
        
        Args:
            string (str): String containing the message to display.
            
        Returns:
            None
        """
        for char in string:
            data = ord(char)
            self._write_data(data)
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
        self.move_to(x, y)
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
        self._write_command(0x40 | (location << 3))
        sleep_us(40)
        for i in range(8):
            self._write_data(charmap[i])
            sleep_us(40)
        self.move_to(self._cursor_x, self._cursor_y)
    
    def _write_init_nibble(self, nibble):
        """
        Writes 4 bits to LCD. Used in __init__.
        
        Args:
            nibble (int): bits to be written.
        
        Returns:
            None
        """
        byte = ((nibble >> 4) & 0x0f) << 4
        self._i2c.writeto(self._i2c_addr, bytes([byte | 4]))
        self._i2c.writeto(self._i2c_addr, bytes([byte]))
        gc.collect()
        
    def _write_command(self, cmd):
        """
        Writes command to LCD. Latched on falling edge of E
        
        Args:
            cmd (int): command to be written.
            
        Returns:
            None
        """
        byte = ((self._backlight << 3) |
                (((cmd >> 4) & 0x0f) << 4))
        self._i2c.writeto(self._i2c_addr, bytes([byte | 4]))
        self._i2c.writeto(self._i2c_addr, bytes([byte]))
        byte = ((self._backlight << 3) |
                ((cmd & 0x0f) << 4))
        self._i2c.writeto(self._i2c_addr, bytes([byte | 4]))
        self._i2c.writeto(self._i2c_addr, bytes([byte]))
        if cmd <= 3:
            sleep_ms(5)
        gc.collect()
        
    def _write_data(self, data):
        """
        Write byte to LCD
        
        Args:
            data (int): byte to write
        
        Returns:
            None
        """
        byte = (1 |
               (self._backlight << 3) |
               (((data >> 4) & 0x0f) << 4))
        self._i2c.writeto(self._i2c_addr, bytes([byte | 4]))
        self._i2c.writeto(self._i2c_addr, bytes([byte]))
        byte = (1 |
               (self._backlight << 3) |
               ((data & 0x0f) << 4))      
        self._i2c.writeto(self._i2c_addr, bytes([byte | 4]))
        self._i2c.writeto(self._i2c_addr, bytes([byte]))
        gc.collect()




