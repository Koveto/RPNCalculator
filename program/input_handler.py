"""
input_handler.py
2/12/2025 Kobe Goodwin

Contains the InputHandler class.

Handles button press interpretation.

Calls appropriate functions based on button labels.
"""

from calculator import Calculator

class InputHandler:
    def __init__(self, lcd):
        """
        Initializes the InputHandler class.

        Args:
            lcd (LCD): An instance of the LCD class.
        """
        self.lcd = lcd
        self.calculator = Calculator(self.lcd)

    def interpret_button_press(self, button_label):
        """
        Interprets the button press and calls the appropriate calculator function.

        Args:
            button_label (str): The label of the button that was pressed.
        """
        unary_buttons = {"Sine", "Cosine", "Tangent", "Arcsine", "Arccosine", "Arctangent",\
                         "Logarithm", "Natural Log", "Negate", "Reciprocal", "Exponential",\
                         "Square", "Power of Ten"}
        binary_buttons = {"Add", "Subtract", "Multiply", "Divide", "Power", "Scientific Notation"}
        digit_buttons = {"0", "1", "2", "3", "4", "5", "6", "7", "8", "9"}

        if button_label in digit_buttons:
            self.calculator.handle_digit_input(button_label)
        elif button_label in unary_buttons:
            self.calculator.unary_operation(button_label)
        elif button_label in binary_buttons:
            self.calculator.binary_operation(button_label)
        elif button_label == "Decimal Point":
            self.calculator.add_decimal_point()
        elif button_label == "Enter":
            self.calculator.calculate_result()
        elif button_label == "Clear":
            self.calculator.clear_display()
        elif button_label == "Backspace":
            self.calculator.delete_last_input()
        elif button_label == "Swap":
            self.calculator.swap_values()

        elif button_label == "Complex Number":
            self.calculator.handle_complex_number()
        elif button_label == "Conjugate":
            self.calculator.calculate_conjugate()
