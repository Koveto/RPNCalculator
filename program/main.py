"""
main.py
Kobe Goodwin
5/7/2025

Initializes I/O, polls button input, interprets presses, updates LCD.
"""

from lcd_i2c import LCD_I2C
from lcd import LCD
from push_buttons import PushButtons
from input_handler import InputHandler
from button_labels import ButtonLabels
from machine import Pin
from time import sleep_ms
import config

# Pinout assignment
# LCD
RS = 21
EN = 20
D4 = 19
D5 = 18
D6 = 17
D7 = 16
SDA = 0
SCL = 1
ANGLE    = [0x00, 0x01, 0x03, 0x06, 0x0C, 0x18, 0x1F, 0x00]
PI       = [0x00, 0x00, 0x1F, 0x0A, 0x0A, 0x0A, 0x0B, 0x00]
SQUARE   = [0x03, 0x05, 0x01, 0x02, 0x07, 0x00, 0x00, 0x00]
ROOT     = [0x04, 0x06, 0x05, 0x04, 0x04, 0x14, 0x0C, 0x04]
DIVIDE   = [0x00, 0x04, 0x00, 0x1F, 0x00, 0x04, 0x00, 0x00]
MULTIPLY = [0x00, 0x11, 0x0A, 0x04, 0x0A, 0x11, 0x00, 0x00]
# Button Array
BUTTON_ROWS = [3, 4, 5, 6, 7, 8, 9]
BUTTON_COLS = [10, 11, 12, 13, 14, 15]

def find_button_index(label):
    """
    Finds the row, column index of a BUTTON_LABELS_A label
    
    Args:
        label (str): The BUTTON_LABELS_A label to retrieve index of
    
    Returns:
        tuple (int, int): The index of the label
    """
    for row_index, row in enumerate(ButtonLabels.BUTTON_LABELS_A):
        if label in row:
            col_index = row.index(label)
            return (row_index, col_index)
    return (0, 0)

def display_settings(lcd):
    """
    Displays config settings
    
    Args:
        lcd (LCD): The display being written to
        
    Returns:
        None
    """
    if ((lcd.rows == 4) and \
        (lcd.columns == 20)):
        
        if (config.orient_top_bottom):
            lcd.write_at(17, 3, "Deg" if config.degrees else "Rad")
        else:
            lcd.write_at(17, 0, "Deg" if config.degrees else "Rad")
            
        if (config.orient_top_bottom):
            lcd.write_at(12, 3, "Polr" if config.polar else "Rect")
        else:
            lcd.write_at(12, 0, "Polr" if config.polar else "Rect")
            
        if (config.orient_top_bottom):
            lcd.write_at(8, 3, "Hex" if config.hexadecimal else "Dec")
        else:
            lcd.write_at(8, 0, "Hex" if config.hexadecimal else "Dec")
            
        if (config.orient_top_bottom):
            lcd.write_at(4, 3, "INF" if config.scientific else "RPN")
        else:
            lcd.write_at(4, 0, "INF" if config.scientific else "RPN")
            
        if (config.button_mode):
            if (config.orient_top_bottom):
                lcd.write_at(0, 3, "2nd")
            else:
                lcd.write_at(0, 0, "2nd")
        else:
            if (config.orient_top_bottom):
                lcd.write_at(0, 3, "   ")
            else:
                lcd.write_at(0, 0, "   ")
                
    elif ((lcd.rows == 2) and \
          (lcd.columns == 16)):
        
        if (config.button_mode):
            lcd.write_at(0, 0, "2nd")
        else:
            lcd.write_at(0, 0, "Y: ")

def main():
    """
    Initializes the I/O
    Polls for button input
    Debounces push button input
    Calls InputHandler for new button presses
    Updates the LCD with new output.
    
    Returns:
        None
    """
    # Initialize I/O
    lcd = LCD(RS, EN, D4, D5, D6, D7)
    #lcd = LCD_I2C(SDA, SCL)
    buttons = PushButtons(BUTTON_ROWS, BUTTON_COLS)
    handler = InputHandler(lcd)
    
    # Custom characters
    lcd.custom_char(0, bytearray(ANGLE))
    lcd.custom_char(1, bytearray(PI))
    lcd.custom_char(2, bytearray(SQUARE))
    lcd.custom_char(3, bytearray(ROOT))
    lcd.custom_char(4, bytearray(DIVIDE))
    lcd.custom_char(5, bytearray(MULTIPLY))
    
    # Initial LCD output
    if ((lcd.rows == 4) and \
        (lcd.columns == 20)):
        lcd.write_at(0, 1, "Z: 0")
        lcd.write_at(0, 2, "Y: 0")
        lcd.write_at(0, 3, "X: 0")
        
    elif ((lcd.rows == 2) and \
          (lcd.columns == 16)):
        lcd.write_at(0, 0, "Y: 0")
        lcd.write_at(0, 1, "X: 0")
    
    # Prevent repeated presses
    previous_press = None
    index_previous = (0, 0)

    # Main loop
    while True:
        button_press = buttons.get_button()
        
        # Determine which function was pressed
        if button_press:
            index_previous = find_button_index(previous_press)
            
        # A new (debounced) button function was pressed...
        if button_press and (button_press != previous_press) and \
           (button_press != ButtonLabels.BUTTON_LABELS_A[index_previous[0]][index_previous[1]]):
            
            # If "2nd"...
            if (button_press == ButtonLabels.ALTERNATE_FUNCTIONS):
                if (config.button_mode):
                    new_buttons = ButtonLabels.BUTTON_LABELS_A
                else:
                    new_buttons = ButtonLabels.BUTTON_LABELS_B
                config.button_mode = not config.button_mode
                buttons.set_key_list(new_buttons)
                
            # Any button that isn't "2nd"...
            else:
                if (config.button_mode):
                    config.button_mode = False
                    buttons.set_key_list(ButtonLabels.BUTTON_LABELS_A)
                handler.interpret_button_press(button_press)
            previous_press = button_press
            
        # None for debouncing
        elif button_press is None:
            previous_press = None
            
        # Update settings    
        display_settings(lcd)
            
        sleep_ms(100)

if __name__ == "__main__":
    main()








