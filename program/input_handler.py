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
        digit_buttons = {"0", "1", "2", "3", "4", "5", "6", "7", "8", "9"}
        operator_buttons = {"Add", "Subtract", "Multiply", "Divide"}
        trig_buttons = {"Sine", "Cosine", "Tangent", "Arcsine", "Arccosine", "Arctangent"}
        log_buttons = {"Logarithm", "Natural Log"}

        if button_label in digit_buttons:
            self.calculator.handle_digit_input(button_label)
        elif button_label == "Decimal Point":
            self.calculator.add_decimal_point()
        elif button_label == "Enter":
            self.calculator.calculate_result()
        elif button_label == "Clear":
            self.calculator.clear_display()
        elif button_label == "Backspace":
            self.calculator.delete_last_input()

        elif button_label in operator_buttons:
            self.calculator.handle_operator_input(button_label)
        elif button_label == "Negate":
            self.calculator.negate_number()
        elif button_label == "Reciprocal":
            self.calculator.calculate_reciprocal()
        elif button_label == "Swap":
            self.calculator.swap_values()

        elif button_label in trig_buttons:
            self.calculator.handle_trigonometric_function(button_label)

        elif button_label in log_buttons:
            self.calculator.handle_logarithm_function(button_label)

        elif button_label == "Exponential":
            self.calculator.calculate_exponential()
        elif button_label == "Scientific Notation":
            self.calculator.convert_to_scientific_notation()
        elif button_label == "Power":
            self.calculator.raise_to_power()
        elif button_label == "Square":
            self.calculator.calculate_square()
        elif button_label == "Power of Ten":
            self.calculator.calculate_power_of_ten()

        elif button_label == "Complex Number":
            self.calculator.handle_complex_number()
        elif button_label == "Conjugate":
            self.calculator.calculate_conjugate()