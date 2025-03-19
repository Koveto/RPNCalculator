"""
main.py
3/2/2025 Kobe Goodwin

Initializes I/O, polls button input, interprets presses, updates LCD.
"""

from lcd import LCD
from push_buttons import PushButtons
from input_handler import InputHandler
from button_labels import ButtonLabels
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
# Button Array
BUTTON_ROWS = [3, 4, 5, 6, 7, 8, 9]
BUTTON_COLS = [10, 11, 12, 13, 14, 15]


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
    if ROWS == 4:
        lcd.write_at(0, 0, "D: 0")
        lcd.write_at(0, 1, "C: 0")
    lcd.write_at(0, ROWS - 2, "B: 0")
    lcd.write_at(0, ROWS - 1, "A: 0")
    
    previous_press = None
    button_mode = False

    # Main loop
    while True:
        button_press = buttons.get_button()
        if button_press and button_press != previous_press:
            if (button_press == ButtonLabels.ALTERNATE_FUNCTIONS):
                if (button_mode):
                    new_buttons = ButtonLabels.BUTTON_LABELS_A
                else:
                    new_buttons = ButtonLabels.BUTTON_LABELS_B
                button_mode = not button_mode
                buttons.set_key_list(new_buttons)
            else:
                if (button_mode):
                    button_mode = False
                    buttons.set_key_list(ButtonLabels.BUTTON_LABELS_A)
                handler.interpret_button_press(button_press)
            previous_press = button_press
        elif button_press is None:
            previous_press = None
        if (button_mode):
            lcd.write_at(lcd.columns - 3, 0, "2nd")
        else:
            lcd.write_at(lcd.columns - 3, 0, "   ")
            
        sleep_ms(100)

if __name__ == "__main__":
    main()


