"""
push_buttons.py
<<<<<<< HEAD:program/push_buttons.py
4/29/2025 Kobe Goodwin
=======
4/25/2025 Kobe Goodwin
>>>>>>> fda07ff5f52634aca81e06061b32d6d8e8982986:program_parallel/push_buttons.py

Module for reading input from a push button array.
"""

from machine import Pin
from button_labels import ButtonLabels

class PushButtons:
    def __init__(self, rowPinNos, colPinNos):
        """
        Initializes the PushButtons class.

        Args:
            rowPinNos (list): List of pin numbers for rows.
            colPinNos (list): List of pin numbers for columns.
        
        Returns:
            Instance of PushButtons
        """
        self.row_list = [Pin(pin, Pin.OUT) for pin in rowPinNos]
        self.col_list = [Pin(pin, Pin.IN, Pin.PULL_UP) for pin in colPinNos]
        self.key_list = ButtonLabels.BUTTON_LABELS_A

        # Set all row pins to high
        for row in self.row_list:
            row.value(1)

    def set_key_list(self, key_list):
        """
        Mutator for key list. See button_labels.py
        
        Args:
            key_list (list): Nested list of string identifiers for each button
                             See button_labels.py
        
        Returns:
            None
        """
        self.key_list = key_list

    def get_button(self):
        """
        Scans the button array and returns the identifier of the pressed button.

        Returns:
            str: The identifier of the pressed button
                 None if no button is pressed.
        """
        for row in self.row_list:
            row.value(0)  # Set the current row to low
            result = [col.value() for col in self.col_list]
            if 0 in result:  # Check if any button in the current row is pressed
                button = self.key_list[self.row_list.index(row)][result.index(0)]
                row.value(1)  # Reset the row to high
                return button
            row.value(1)
        return None


