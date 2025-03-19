"""
main.py
3/3/2025 Kobe Goodwin

LCD TEST MODULE
"""

from lcd import LCD
from machine import Pin
from time import sleep_ms

# Pinout assignment
# LCD
COLUMNS = 20
ROWS = 4
RS = 21
EN = 20
D4 = 19
D5 = 18
D6 = 17
D7 = 16


def main():
    """
    The main method initializes the I/O, polls for button input, debounces
    push button input, calls InputHandler for new button presses, and updates 
    the LCD with new output.
    """
    # Initialize I/O
    lcd = LCD(ROWS, COLUMNS, RS, EN, D4, D5, D6, D7)
    
    # Initial LCD output
    if ROWS == 4:
        lcd.write_at(0, 0, "main.py")
        lcd.write_at(0, 1, "Kobe Goodwin")
    lcd.write_at(0, ROWS - 2, "Y: 0")
    lcd.write_at(0, ROWS - 1, "X: 0")

    # Main loop
    while True:
        sleep_ms(100)

if __name__ == "__main__":
    main()


