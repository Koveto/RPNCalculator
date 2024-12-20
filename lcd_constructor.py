from machine import Pin
from gpio_lcd import GpioLcd

def getLCD(col, row, Rs, E, D4, D5, D6, D7):
    lcd = GpioLcd(rs_pin=Pin(Rs),
              enable_pin=Pin(E),
              d4_pin=Pin(D4),
              d5_pin=Pin(D5),
              d6_pin=Pin(D6),
              d7_pin=Pin(D7),
              num_lines=row, num_columns=col)
    return lcd
