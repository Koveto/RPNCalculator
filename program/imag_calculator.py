import math
import cmath
from stack import Stack

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

    def handle_complex_number(self):
        """
        Handles complex number input by creating a complex number from the
        top two numbers on the stack and updates the display.
        """
        if self.input_in_progress:
            self.stack.push(float(self.current_input))
            self.current_input = ""
            self.input_in_progress = False
        
        if self.stack.size() < 2:
            return

        x = self.stack.pop()
        y = self.stack.pop()
        complex_number = complex(y, x)
        self.stack.push(complex_number)
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

    def calculate_result(self):
        """
        Finalizes the current input, pushes it to the stack, and updates the LCD display.
        """
        if self.current_input:
            try:
                self.stack.push(float(self.current_input))
            except ValueError:
                self.current_input = ""
                self.update_display()
                return
            self.current_input = ""
        else:
            self.stack.push(self.stack.peek())
        
        self.input_in_progress = False
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

    def handle_operator_input(self, operator):
        """
        Handles arithmetic operations using the top number on the stack (y)
        and the current input number (x).

        Args:
            operator (str): A string representing the operation ("Add", "Subtract", "Multiply", "Divide").
        """
        if self.stack.is_empty():
            y = 0.0
        else:
            y = self.stack.pop()
        if self.current_input:
            x = float(self.current_input)
        else:
            x = y
            if self.stack.is_empty():
                y = 0.0
            else:
                y = self.stack.pop()
        result = None

        if operator == "Add":
            result = y + x
        elif operator == "Subtract":
            result = y - x
        elif operator == "Multiply":
            result = y * x
        elif operator == "Divide":
            if x != 0:
                result = y / x

        if result is not None:
            self.stack.push(result)
            self.current_input = ""
            self.input_in_progress = False
            self.update_display()

    def unary_operation(self, op):
        """
        Performs a unary operation on the top number on the stack.

        Args:
            op (str): A string representing the operation.
                      Valid operations are: "Natural Log", "Exponential", "Logarithm",
                      "Power of Ten", "Square", "Sine", "Cosine", "Tangent",
                      "Arcsine", "Arccosine", "Arctangent", "Negate", "Reciprocal".
        """
        if not self.input_in_progress and self.stack.is_empty():
            return

        if self.input_in_progress:
            self.stack.push(float(self.current_input))
            self.current_input = ""
            self.input_in_progress = False
        
        x = self.stack.pop() if not self.stack.is_empty() else 0.0
        result = None

        if op == "Natural Log":
            if x == 0.0:
                self.stack.push(x)
                return
            result = math.log(x)
        elif op == "Exponential":
            result = math.exp(x)
        elif op == "Logarithm":
            if x == 0.0:
                self.stack.push(x)
                return
            result = math.log10(x)
        elif op == "Power of Ten":
            result = 10**x
        elif op == "Square":
            result = x**2
        elif op == "Sine":
            result = math.sin(x)
        elif op == "Cosine":
            result = math.cos(x)
        elif op == "Tangent":
            result = math.tan(x)
        elif op == "Arcsine":
            result = math.asin(x)
        elif op == "Arccosine":
            result = math.acos(x)
        elif op == "Arctangent":
            result = math.atan(x)
        elif op == "Negate":
            result = -x
        elif op == "Reciprocal":
            if (x == 0.0):
                self.stack.push(x)
                return
            result = 1 / x

        if result is not None:
            self.stack.push(result)
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

        if op == "Add":
            result = y + x
        elif op == "Subtract":
            result = y - x
        elif op == "Multiply":
            result = y * x
        elif op == "Divide":
            if x != 0:
                result = y / x
        elif op == "Power":
            result = y**x
        elif op == "Scientific Notation":
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
        max_length = self.lcd.columns - 3
        real_part = f"{cnum.real:.2e}".replace("+", "")
        imag_part = f"{cnum.imag:.2e}".replace("+", "")
        
        # Construct the full string
        result = f"{real_part} + j{imag_part}"
        
        # Truncate to fit within max_length
        if len(result) > max_length:
            truncated_real = f"{cnum.real:.1e}".replace("+", "")
            truncated_imag = f"{cnum.imag:.1e}".replace("+", "")
            result = f"{truncated_real} + j{truncated_imag}"
            if len(result) > max_length:
                split_real = truncated_real.split("e")
                split_imag = truncated_imag.split("e")
                #result = f"{split_real[0]}
        
        result = result[:max_length]
        result += ' ' * (self.lcd.columns - 3 - len(result))
        
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



