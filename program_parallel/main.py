"""
main.py
Kobe Goodwin

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
    Displays 2nd and DEG/RAD settings.
    
    Args:
        lcd (LCD): The display being written to
    """
    if (config.orient_top_bottom):
        lcd.write_at(lcd.columns - 3, 3, "DEG" if config.degrees else "RAD")
    else:
        lcd.write_at(lcd.columns - 3, 0, "DEG" if config.degrees else "RAD")
    if (config.orient_top_bottom):
        lcd.write_at(lcd.columns - 7, 3, "POL" if config.polar else "REC")
    else:
        lcd.write_at(lcd.columns - 7, 0, "POL" if config.polar else "REC")
    if (config.button_mode):
        if (config.orient_top_bottom):
            lcd.write_at(lcd.columns - 11, 3, "2nd")
        else:
            lcd.write_at(lcd.columns - 11, 0, "2nd")
    else:
        if (config.orient_top_bottom):
            lcd.write_at(lcd.columns - 11, 3, "   ")
        else:
            lcd.write_at(lcd.columns - 11, 0, "   ")

def main():
    """
    The main method initializes the I/O, polls for button input, debounces
    push button input, calls InputHandler for new button presses, and updates 
    the LCD with new output.
    """
    # Initialize I/O
    lcd = LCD(ROWS, COLUMNS, RS, EN, D4, D5, D6, D7)
    buttons = PushButtons(BUTTON_ROWS, BUTTON_COLS)
    handler = InputHandler(lcd)
    
    # Initial LCD output
    lcd.write_at(0, 0, "D: 0")
    lcd.write_at(0, 1, "C: 0")
    lcd.write_at(0, 2, "B: 0")
    lcd.write_at(0, 3, "A: 0")
    
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
                        lcd.write_at(lcd.columns - 7, 3, "   ")
                    else:
                        lcd.write_at(lcd.columns - 7, 0, "   ")
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



