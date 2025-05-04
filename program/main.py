"""
main.py
Kobe Goodwin
4/30/2025

Initializes I/O, polls button input, interprets presses, updates LCD.
"""

from lcd import LCD
from push_buttons import PushButtons
from input_handler import InputHandler
from button_labels import ButtonLabels
from machine import Pin
from time import sleep_ms
import config

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
    lcd = LCD(ROWS, COLUMNS, RS, EN, D4, D5, D6, D7)
    buttons = PushButtons(BUTTON_ROWS, BUTTON_COLS)
    handler = InputHandler(lcd)
    
    # Initial LCD output
    lcd.write_at(0, 1, "Z: 0")
    lcd.write_at(0, 2, "Y: 0")
    lcd.write_at(0, 3, "X: 0")
    
    # Prevent repeated presses
    previous_press = None
    index_previous = (0, 0)

    # Main loop
    while True:
        button_press = buttons.get_button()
        if button_press:
            index_previous = find_button_index(previous_press)
        if button_press and (button_press != previous_press) and \
           (button_press != ButtonLabels.BUTTON_LABELS_A[index_previous[0]][index_previous[1]]):
            if (button_press == ButtonLabels.ALTERNATE_FUNCTIONS):
                if (config.button_mode):
                    new_buttons = ButtonLabels.BUTTON_LABELS_A
                    if (config.orient_top_bottom):
                        lcd.write_at(lcd.columns - 20, 3, "   ")
                    else:
                        lcd.write_at(lcd.columns - 3, 0, "   ")
                else:
                    new_buttons = ButtonLabels.BUTTON_LABELS_B
                config.button_mode = not config.button_mode
                buttons.set_key_list(new_buttons)
            else:
                if (config.button_mode):
                    config.button_mode = False
                    buttons.set_key_list(ButtonLabels.BUTTON_LABELS_A)
                handler.interpret_button_press(button_press)
            previous_press = button_press
        elif button_press is None:
            previous_press = None
        display_settings(lcd)
            
        sleep_ms(100)

if __name__ == "__main__":
    main()



