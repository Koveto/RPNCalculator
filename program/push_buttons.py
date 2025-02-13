"""
push_buttons.py
2/12/2025 Kobe Goodwin

Module for reading input from a push button array.
"""

from machine import Pin

class PushButtons:
    def __init__(self, rowPinNos, colPinNos, buttonList):
        """
        Initializes the PushButtons class.

        Args:
            rowPinNos (list): List of pin numbers for rows.
            colPinNos (list): List of pin numbers for columns.
            buttonList (list): Nested list of string identifiers for each button.
        """
        self.row_list = [Pin(pin, Pin.OUT) for pin in rowPinNos]
        self.col_list = [Pin(pin, Pin.IN, Pin.PULL_UP) for pin in colPinNos]
        self.key_list = buttonList

        # Set all row pins to high
        for row in self.row_list:
            row.value(1)

    def get_button(self):
        """
        Scans the button array and returns the identifier of the pressed button.

        Returns:
            str: The identifier of the pressed button, or None if no button is pressed.
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