"""
input_handler.py
Kobe Goodwin
4/25/2025

Contains the InputHandler class.
Handles button press interpretation.
Calls appropriate functions based on button labels.
"""

from calculator import Calculator
from calculator import UndefinedError
from button_labels import ButtonLabels as b
import config

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
        unary_buttons = {b.SINE, b.COSINE, b.TANGENT, b.ARCSINE, b.ARCCOSINE, b.ARCTANGENT,
                         b.LOGARITHM, b.NATURAL_LOG, b.NEGATE, b.RECIPROCAL, b.EXPONENTIAL,
                         b.SQUARE, b.POWER_OF_TEN, b.CONJUGATE, b.SQRT, b.ABS, b.ANGLE,
                         b.REAL, b.IMAG, b.DEG, b.RAD, b.ROUND, b.GAMMA}
        binary_buttons = {b.ADD, b.SUBTRACT, b.MULTIPLY, b.DIVIDE, b.POWER,
                          b.SCIENTIFIC_NOTATION, b.PERCENT, b.MODULUS}
        digit_buttons = {b.ZERO, b.ONE, b.TWO, b.THREE, b.FOUR, b.FIVE, b.SIX, b.SEVEN,
                         b.EIGHT, b.NINE, b.E, b.AHEX, b.BHEX, b.CHEX, b.DHEX, b.EHEX,
                         b.FHEX}

        try:
            if button_label in digit_buttons:
                self.calculator.handle_digit_input(button_label)
            elif button_label in unary_buttons:
                self.calculator.unary_operation(button_label)
            elif button_label in binary_buttons:
                self.calculator.binary_operation(button_label)

            elif button_label == b.DECIMAL_POINT:
                self.calculator.add_decimal_point()
            elif button_label == b.COMPLEX_NUMBER:
                self.calculator.handle_complex_number()
            elif button_label == b.COMPLEX_POLAR:
                self.calculator.handle_complex_number(polar=True)
            elif button_label == b.SPLIT_COMPLEX_POLAR:
                self.calculator.split_complex_polar()
            elif button_label == b.SPLIT_COMPLEX_RECT:
                self.calculator.split_complex_rect()

            elif button_label == b.ENTER:
                self.calculator.calculate_result()
                self.calculator.just_pressed_enter = True
            elif button_label == b.CLEAR:
                self.calculator.clear_display()
            elif button_label == b.BACKSPACE:
                self.calculator.delete_last_input()
            elif button_label == b.SWAP:
                self.calculator.swap_values()
            elif button_label == b.SUM_PLUS:
                self.calculator.sum_function()
            elif button_label == b.SUM_MINUS:
                self.calculator.sum_function(True)
            elif button_label == b.MEAN:
                self.calculator.mean()

            elif button_label == b.PI:
                self.calculator.pi()
            elif button_label == b.STO:
                self.calculator.store_number()
            elif button_label == b.RCL:
                self.calculator.recall_number()
            elif button_label == b.ROLL:
                self.calculator.roll()
                
            elif button_label == b.RADDEG:
                config.degrees = not config.degrees
            elif button_label == b.RECPOL:
                config.polar = not config.polar
            elif button_label == b.ORIENT:
                config.orient_top_bottom = not config.orient_top_bottom
            elif button_label == b.HEXADECIMAL:
                config.hexadecimal = not config.hexadecimal
            elif button_label == b.SCIENTIFIC:
                config.scientific = not config.scientific
                
            if (button_label != b.ENTER and \
                self.calculator.just_pressed_enter):
                self.calculator.just_pressed_enter = False
            self.calculator.update_display()

        except ZeroDivisionError as zde:
            if config.orient_top_bottom:
                r = self.lcd.rows - 2
            else:
                r = self.lcd.rows - 3
            self.lcd.write_at(0, r, "Divide by zero error")
            print(f"Error: {zde}")
        except UndefinedError as ue:
            if config.orient_top_bottom:
                r = self.lcd.rows - 2
            else:
                r = self.lcd.rows - 3
            self.lcd.write_at(0, r, "Domain error        ")
            print(f"Error: {ue}")
        except Exception as e:
            if config.orient_top_bottom:
                r = self.lcd.rows - 2
            else:
                r = self.lcd.rows - 3
            self.lcd.write_at(0, r, "ERROR!              ")
            print(f"Error: {e}")


