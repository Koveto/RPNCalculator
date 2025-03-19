"""
calculator.py
Kobe Goodwin

Calculator for performing arithmetic and trigonometric operations,
including support for complex numbers, using an LCD display for
output visualization.
"""


import math
import cmath
from stack import Stack
from button_labels import ButtonLabels as b

class Calculator:
    def __init__(self, lcd):
        """
        Initializes the Calculator with the given LCD instance.

        Args:
            lcd (LCD): An instance of the LCD class.
        """
        self.lcd = lcd
        self.stack = Stack()
        self.current_input = ""
        self.input_in_progress = False

        # Initialize LCD display
        self.lcd.write_at(0, 0, "Y: 0.0000")
        self.lcd.write_at(0, 1, "X: 0.0000")

    def handle_complex_number(self, update_display = True):
        """
        Handles complex number input by creating a complex number from the
        top two numbers on the stack and updates the display.
        
        Args:
        update_display (bool): A boolean representing whether to
                                   update the display or not, typically
                                   True.
        """
        if self.input_in_progress:
            self.stack.push(float(self.current_input))
            self.current_input = ""
            self.input_in_progress = False
        
        if self.stack.size() < 2:
            self.update_display()
            return

        x = self.stack.pop()
        y = self.stack.pop()
        complex_number = complex(y, x)
        self.stack.push(complex_number)
        if update_display:
            self.update_display()


    def handle_digit_input(self, digit):
        """
        Handles digit input, updating the current input and LCD display.

        Args:
            digit (str): A digit character ("0" to "9").
        """
        if self.input_in_progress:
            self.current_input += digit
        else:
            if self.current_input:
                self.stack.push(float(self.current_input))
                self.current_input = digit
            else:
                self.current_input = digit
            self.input_in_progress = True
        
        self.update_display()

    def add_decimal_point(self):
        """
        Adds a decimal point to the current input.
        """
        if self.input_in_progress:
            if "." not in self.current_input:
                self.current_input += "."
        else:
            if self.current_input:
                self.stack.push(float(self.current_input))
            self.current_input = "0."
            self.input_in_progress = True
        
        self.update_display()

    def calculate_result(self, update_display = True):
        """
        Finalizes the current input, pushes it to the stack, and updates
        the LCD display.
        
        Args:
            update_display (bool): Whether to update the display or not. Default is True.
        """
        if self.current_input:
            try:
                self.stack.push(float(self.current_input))
            except ValueError:
                self.current_input = ""
                self.update_display()
                return
            self.current_input = ""
        elif not self.stack.is_empty():
            self.stack.push(self.stack.peek())
        
        self.input_in_progress = False
        if (update_display):
            self.update_display()

    def clear_display(self):
        """
        Empties the stack and clears the input. Resets the display to the startup state.
        """
        self.stack = Stack()
        self.current_input = ""
        self.input_in_progress = False
        self.lcd.write_at(0, 0, "Y: 0.0000" + (" " * (self.lcd.columns - 9)))
        self.lcd.write_at(0, 1, "X: 0.0000" + (" " * (self.lcd.columns - 9)))

    def delete_last_input(self):
        """
        Removes the last digit or decimal point if a number is in progress.
        Resets the X row to 0 if the input is one digit or if no input is in progress.
        """
        if self.input_in_progress:
            if len(self.current_input) > 1:
                self.current_input = self.current_input[:-1]
            else:
                self.current_input = ""
                self.input_in_progress = False
        else:
            self.stack.pop()
        
        self.update_display()
        
    def pi(self):
        """
        Adds an approximation of pi to the top of the stack.
        """
        self.calculate_result(update_display = False)
        self.current_input = str(cmath.pi)
        self.calculate_result()
        
    def split_complex_polar(self):
        """
        Pops top number from stack (or input).
        Pushes Absolute Value then Angle
        """
        # unary_operation("Abs")
        if not self.input_in_progress and self.stack.is_empty():
            return
        if self.input_in_progress:
            self.stack.push(float(self.current_input))
            self.current_input = ""
            self.input_in_progress = False
        x = self.stack.pop() if not self.stack.is_empty() else 0.0
        result = abs(x)
        self.stack.push(result)
        
        # Get x to the top of the stack
        self.input_in_progress = True
        self.current_input = str(x)
        if (type(x) == complex):
            self.current_input = str(x.real)
            self.calculate_result(update_display = False)
            self.current_input = str(x.imag)
            self.calculate_result(update_display = False)
            self.handle_complex_number(update_display = False)
            
        self.unary_operation(b.ANGLE)
        
    def split_complex_rect(self):
        """
        Pops top number from stack (or input).
        Pushes Rect then Imag
        """
        # unary_operation("Real")
        if not self.input_in_progress and self.stack.is_empty():
            return
        if self.input_in_progress:
            self.stack.push(float(self.current_input))
            self.current_input = ""
            self.input_in_progress = False
        x = self.stack.pop() if not self.stack.is_empty() else 0.0
        if (type(x) == complex):
            result = x.real
        else:
            result = x
        self.stack.push(result)
        
        # Get x to the top of the stack
        self.input_in_progress = True
        self.current_input = str(x)
        if (type(x) == complex):
            self.current_input = str(x.real)
            self.calculate_result(update_display = False)
            self.current_input = str(x.imag)
            self.calculate_result(update_display = False)
            self.handle_complex_number(update_display = False)
            
        self.unary_operation(b.IMAG)

    def unary_operation(self, op, update_display = True):
        """
        Performs a unary operation on the top number on the stack.

        Args:
            op (str): A string representing the operation.
                      Valid operations are: "Natural Log", "Exponential", "Logarithm",
                      "Power of Ten", "Square", "Sine", "Cosine", "Tangent",
                      "Arcsine", "Arccosine", "Arctangent", "Negate", "Reciprocal",
                      "Conjugate", "Sqrt", "Abs", "Angle", "Real", "Imag"
            update_display (bool): Whether to update the display or not. Default is True.
        """
        if not self.input_in_progress and self.stack.is_empty():
            return

        if self.input_in_progress:
            self.stack.push(float(self.current_input))
            self.current_input = ""
            self.input_in_progress = False
        
        x = self.stack.pop() if not self.stack.is_empty() else 0.0
        result = None

        if op == b.NATURAL_LOG:
            if x == 0.0:
                self.stack.push(x)
                return
            result = math.log(x)
        elif op == b.EXPONENTIAL:
            result = math.exp(x)
        elif op == b.LOGARITHM:
            if x == 0.0:
                self.stack.push(x)
                return
            result = math.log10(x)
        elif op == b.POWER_OF_TEN:
            result = 10**x
        elif op == b.SQUARE:
            result = x**2
        elif op == b.SQRT:
            result = x ** (1/2)
        elif op == b.SINE:
            result = math.sin(x)
        elif op == b.COSINE:
            result = math.cos(x)
        elif op == b.TANGENT:
            result = math.tan(x)
        elif op == b.ARCSINE:
            result = math.asin(x)
        elif op == b.ARCCOSINE:
            result = math.acos(x)
        elif op == b.ARCTANGENT:
            result = math.atan(x)
        elif op == b.NEGATE:
            result = -x
        elif op == b.CONJUGATE:
            if (type(x) == complex):
                result = complex(x.real, -x.imag)
        elif op == b.RECIPROCAL:
            if (x == 0.0):
                self.stack.push(x)
                return
            result = 1 / x
        elif op == b.ABS:
            result = abs(x)
        elif op == b.ANGLE:
            result = cmath.phase(x)
        elif op == b.REAL:
            if (type(x) == complex):
                result = x.real
            else:
                result = x
        elif op == b.IMAG:
            if (type(x) == complex):
                result = x.imag
            else:
                result = 0.0

        if result is not None:
            self.stack.push(result)
            if update_display:
                self.update_display()
            
    def binary_operation(self, op):
        """
        Performs a binary operation on the top two numbers on the stack.

        Args:
            op (str): A string representing the operation.
                      Valid operations are: "Add", "Subtract", "Multiply", "Divide", "Power", "Scientific Notation".
        """
        if self.input_in_progress:
            self.stack.push(float(self.current_input))
            self.current_input = ""
            self.input_in_progress = False
        
        x = self.stack.pop() if not self.stack.is_empty() else 0.0
        y = self.stack.pop() if not self.stack.is_empty() else 0.0
        result = None

        if op == b.ADD:
            result = y + x
        elif op == b.SUBTRACT:
            result = y - x
        elif op == b.MULTIPLY:
            result = y * x
        elif op == b.DIVIDE:
            if x != 0:
                result = y / x
        elif op == b.POWER:
            result = y**x
        elif op == b.SCIENTIFIC_NOTATION:
            result = y * (10**x)

        if result is not None:
            self.stack.push(result)
            self.update_display()

    def swap_values(self):
        """
        Pushes the in-progress number to the stack if any.
        Swaps the two values at the top of the stack and updates the display.
        """
        if self.input_in_progress:
            self.stack.push(float(self.current_input))
            self.current_input = ""
            self.input_in_progress = False
        
        if self.stack.size() >= 2:
            x = self.stack.pop()
            y = self.stack.pop()
            self.stack.push(x)
            self.stack.push(y)
        
        self.update_display()

    def format_complex_number(self, cnum):
        """
        Formats a complex number as a string in rectangular form to fit within the lcd.columns - 3 length.
        
        Args:
            cnum (complex): The complex number to format.
            
        Returns:
            str: The formatted string representing the complex number.
        """
        #print("Complex number! " + str(cnum))
        max_length = self.lcd.columns - 3
        real_part = f"{cnum.real:.2e}".replace("+", "")
        imag_part = f"{cnum.imag:.2e}".replace("+", "")
        
        # Construct the full string
        result = f"{real_part}+j{imag_part}"
        #print("Initially... " + str(result))
        
        # Truncate to fit within max_length
        if len(result) > max_length:
            truncated_real = f"{cnum.real:.1e}".replace("+", "")
            truncated_imag = f"{cnum.imag:.1e}".replace("+", "")
            result = f"{truncated_real}+j{truncated_imag}"
            #print("Rev 1... " + str(result))
            """if len(result) > max_length:
                result = result.replace(".0","")
                r = int(cnum.real)
                i = int(cnum.imag)
                truncated_real = f"{r:.0e}".replace("+","")
                truncated_imag = f"{i:.0e}".replace("+","")
                result = f"{truncated_real}+j{truncated_imag}"
                print("Rev 2... " + str(result))"""
        
        result = result[:max_length]
        result += ' ' * (self.lcd.columns - 3 - len(result))
        
        #print("Display... " + str(result))
        
        return result
    
    
    
    def update_display(self):
        """
        Updates the LCD display based on the current state.
        """
        if self.input_in_progress:
            x_value = self.current_input
            if len(x_value) > self.lcd.columns - 4:  # Adjusting for "..." and "_"
                x_display = "..." + x_value[-(self.lcd.columns - 4):] + "_"
            else:
                x_display = f"X: {x_value}_"
            y_value = self.stack.stack[-1] if self.stack.size() > 0 else 0.0000
        else:
            x_value = self.stack.peek() if not self.stack.is_empty() else "0.0000"
            if isinstance(x_value, complex):
                # Format complex number for display
                x_display = "X: " + self.format_complex_number(x_value)
            else:
                x_display = f"X: {float(x_value):.4g}"  # Use general format for large/small numbers
            y_value = self.stack.stack[-2] if self.stack.size() > 1 else 0.0000

        # Create strings with trailing spaces to ensure they are of length lcd.columns
        if isinstance(y_value, complex):
            # Format complex number for display
            y_display = "Y: " + self.format_complex_number(y_value)
        else:
            y_display = f"Y: {y_value:.4g}"  # Use general format for large/small numbers
            y_display += ' ' * (self.lcd.columns - len(y_display))

        x_display += ' ' * (self.lcd.columns - len(x_display))
        
        
        # Write to the LCD
        self.lcd.write_at(0, 0, y_display)
        self.lcd.write_at(0, 1, x_display)
        
        print(self.stack)





