"""
main.py
3/3/2025 Kobe Goodwin

BUTTON TEST PROGRAM
"""

from push_buttons import PushButtons
from button_labels import ButtonLabels
from time import sleep_ms

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
    buttons = PushButtons(BUTTON_ROWS, BUTTON_COLS)
    
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
                button_mode = not button_mode
                print(ButtonLabels.ALTERNATE_FUNCTIONS)
            else:
                print(button_press)
            previous_press = button_press
        elif button_press is None:
            previous_press = None
            
        sleep_ms(100)

if __name__ == "__main__":
    main()


