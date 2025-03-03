"""
main.py
2/25/2025 Kobe Goodwin

Initializes I/O, polls button input, interprets presses, updates LCD.
"""

from lcd import LCD
from push_buttons import PushButtons
from input_handler import InputHandler
from button_labels import ButtonLabels
from time import sleep_ms

# Pinout assignment
# LCD
COLUMNS = 16
ROWS = 2
SDA = 0
SCL = 1
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
    lcd = LCD(COLUMNS, ROWS, SDA, SCL)
    buttons = PushButtons(BUTTON_ROWS, BUTTON_COLS)
    handler = InputHandler(lcd)
    
    # Initial LCD output
    if ROWS == 4:
        lcd.write_at(0, 0, "rpnCalculator.py")
        lcd.write_at(0, 1, "Kobe Goodwin")
    lcd.write_at(0, ROWS - 2, "Y: 0")
    lcd.write_at(0, ROWS - 1, "X: 0")
    
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
                buttons.set_key_list(new_buttons)
            else:
                handler.interpret_button_press(button_press)
            previous_press = button_press
        elif button_press is None:
            previous_press = None
            
        sleep_ms(100)

if __name__ == "__main__":
    main()

