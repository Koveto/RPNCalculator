"""
Calculator for handling reverse polish notation (RPN) inputs.

Fields:
- lcd: Instance of the LCD class.
- stack: Instance of the Stack class.
- current_input: Keeps track of the current number being input.
- input_in_progress: Boolean flag to indicate if a number is in the process of being input.

Methods:
- __init__(self, lcd): Initializes the calculator and updates the LCD display with the initial values.
- handle_digit_input(self, digit): Handles digit input and updates the LCD display.
- add_decimal_point(self): Adds a decimal point to the current input.
- calculate_result(self): Finalizes the current input, pushes it to the stack, and updates the LCD display.
- clear_display(self): Empties the stack and clears the input, resetting the display to the startup state.
- delete_last_input(self): Removes the last digit or decimal point if a number is in progress, or resets the X row to 0.
- handle_operator_input(self, operator): Handles arithmetic operations using the top two numbers on the stack.
- update_display(self): Updates the LCD display based on the current state.
"""

import math
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
                self.current_input = "0"
                self.input_in_progress = False
        else:
            self.current_input = "0"
            self.input_in_progress = True
        
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
            
    def negate_number(self):
        """
        Solves X = -X and updates the display.
        """
        if self.input_in_progress:
            self.current_input = str(-float(self.current_input))
        else:
            if not self.stack.is_empty():
                x = self.stack.pop()
                self.stack.push(-x)
        self.update_display()
    
    def calculate_reciprocal(self):
        """
        Solves X = 1/X and updates the display.
        """
        if self.input_in_progress:
            self.current_input = str(1 / float(self.current_input))
        else:
            if not self.stack.is_empty():
                x = self.stack.pop()
                if x != 0:
                    self.stack.push(1 / x)
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

    def handle_trigonometric_function(self, trig_function):
        """
        Handles trigonometric functions on the top number on the stack.

        Args:
            trig_function (str): A string representing the trig function 
                                 ("Sine", "Cosine", "Tangent", "Arcsine", "Arccosine", "Arctangent").
        """
        if self.input_in_progress:
            self.stack.push(float(self.current_input))
            self.current_input = ""
            self.input_in_progress = False
        
        if not self.stack.is_empty():
            x = self.stack.pop()
            if trig_function == "Sine":
                result = math.sin(x)
            elif trig_function == "Cosine":
                result = math.cos(x)
            elif trig_function == "Tangent":
                result = math.tan(x)
            elif trig_function == "Arcsine":
                result = math.asin(x)
            elif trig_function == "Arccosine":
                result = math.acos(x)
            elif trig_function == "Arctangent":
                result = math.atan(x)
            
            self.stack.push(result)
            self.update_display()

    def handle_logarithm_function(self, log_function):
        """
        Handles logarithmic functions on the top number on the stack.

        Args:
            log_function (str): A string representing the log function ("Logarithm", "Natural Log").
        """
        if self.input_in_progress:
            self.stack.push(float(self.current_input))
            self.current_input = ""
            self.input_in_progress = False
        
        if not self.stack.is_empty():
            x = self.stack.pop()
            if log_function == "Logarithm":
                result = math.log10(x)
            elif log_function == "Natural Log":
                result = math.log(x)
            
            self.stack.push(result)
            self.update_display()

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
            x_display = f"X: {float(x_value):.4g}"  # Use general format for large/small numbers
            y_value = self.stack.stack[-2] if self.stack.size() > 1 else 0.0000

        # Create strings with trailing spaces to ensure they are of length lcd.columns
        y_display = f"Y: {y_value:.4g}"  # Use general format for large/small numbers
        y_display += ' ' * (self.lcd.columns - len(y_display))

        x_display += ' ' * (self.lcd.columns - len(x_display))

        # Write to the LCD
        self.lcd.write_at(0, 0, y_display)
        self.lcd.write_at(0, 1, x_display)
        
        # For debugging purposes, print the stack
        print(self.stack)

