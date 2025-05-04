"""
calculator.py
Kobe Goodwin
4/30/2025

Keeps track of the stack and user input.
Displays new output to screen.
"""

import math
import cmath
from stack import Stack
from button_labels import ButtonLabels as b
import config
import os

FILENAME = "variables.txt"

"""
Unique error to be inherited
"""
class CustomError(Exception):
    pass

"""
Domain error
"""
class UndefinedError(CustomError):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class Calculator:
    def __init__(self, lcd):
        """
        Initializes the Calculator with the given LCD instance.

        Args:
            lcd (LCD): draw text to screen
            
        Returns:
            instance of Calculator
        """
        self.lcd = lcd
        self.stack = Stack()
        self.current_input = ""
        self.input_in_progress = False
        self.store = [0.0]*6
        self.just_pressed_enter = False
        if (config.orient_top_bottom):
            self.lcd.write_at(0, 0, "X: 0")
            self.lcd.write_at(0, 1, "Y: 0")
            self.lcd.write_at(0, 2, "Z: 0")
        else:
            self.lcd.write_at(0, 1, "Z: 0")
            self.lcd.write_at(0, 2, "Y: 0")
            self.lcd.write_at(0, 3, "X: 0")
        
    def roll(self):
        """
        Roll stack down: X to bottom, Y to top
        
        Returns:
            None
        """
        self._complete_input()
        if (self.stack.is_empty()):
            return
        self.stack = self.stack + self.stack.pop()
        
    def store_prompt(self):
        """
        Start the store mode
        
        Returns:
            None
        """
        self._complete_input()
        config.storing = True
        
    def store_variable(self, index):
        """
        Store the identifier A-F
        
        Returns:
            None
        """
        try:
            file = open(FILENAME, "r")
            contents = file.read().strip()
            file.close()
        except OSError:
            with open(FILENAME, "w") as file:
                file.write(",".join(["0"] * 6))
            contents = ",".join(["0"] * 6)
        values = contents.split(",")
        values[index] = str(self.stack.peek())
        with open(FILENAME, "w") as file:
            file.write(",".join(values))
        
    def recall_prompt(self):
        """
        Start the recall mode
        
        Returns:
            None
        """
        self._complete_input()
        config.recalling = True
        
    def recall_variable(self, index):
        """
        Recall the identifier A-F
        
        Returns:
            None
        """
        try:
            file = open(FILENAME, "r")
            contents = file.read().strip()
            file.close()
        except OSError:
            with open(FILENAME, "w") as file:
                file.write(",".join(["0"] * 6))
            contents = ",".join(["0"] * 6)
        values = contents.split(",")
        value = values[index]
        print(value)
        if "j" in value:
            self.stack.push(self._str_to_complex(value))
        else:
            self.stack.push(float(value))
            
    def _str_to_complex(self, s):
        """
        Converts a string in the form '(real+imaginaryj)' to a complex number.

        Args:
            s (str): The string representing a complex number '(5+5j)'.

        Returns:
            complex: The complex number represented by the string.
        """
        s = s.strip()
        if s.startswith("(") and s.endswith(")"):
            s = s[1:-1]

        s = s.replace("j", "")
        real = 0.0
        imaginary = 0.0

        if "+" in s:
            parts = s.split("+")
            real = float(parts[0])
            imaginary = float(parts[1])
        elif "-" in s[1:]:
            flag = False
            n = s
            if (s[0] == "-"):
                n = s[1:]
                flag = True
            parts = n.split("-")
            if flag:
                parts[0] = "-" + parts[0]
            real = float(parts[0])
            imaginary = -float(parts[1])
        else:
            if s:
                imaginary = float(s)

        return complex(real, imaginary)
    
    def delete(self):
        """
        Pops the top number
        """
        self._complete_input()
        self.stack.pop()

    def handle_complex_number(self, polar = False):
        """
        Handles complex number input by creating a complex number from the
        top two numbers on the stack and updates the display.
        
        Args:
            polar (bool): True for interpreting Y<X.
                          False for Y+jX
                          
        Returns:
            None
        """
        if (polar):
            config.polar = True
        else:
            config.polar = False
            
        if self.stack.size() == 0:
            self.stack.push(0.0)
        
        self._complete_input()

        if (type(self.stack.peek()) == complex):
            if (polar):
                self.split_complex_polar()
            else:
                self.split_complex_rect()
            return

        x = self.stack.pop()
        y = self.stack.pop()
        
        if (polar):
            if (config.degrees):
                if (type(x) == complex):
                    real = y * cmath.cos(x*math.pi/180)
                else:
                    real = y * math.cos(x*math.pi/180)
                if (type(y) == complex):
                    imag = y * cmath.sin(x*math.pi/180)
                else:
                    imag = y * math.sin(x*math.pi/180)
                complex_number = complex(real, imag)
            else:
                if (type(x) == complex):
                    real = y * cmath.cos(x)
                else:
                    real = y * math.cos(x)
                if (type(y) == complex):
                    imag = y * cmath.sin(x)
                else:
                    imag = y * math.sin(x)
                complex_number = complex(real, imag)
        else:
            complex_number = complex(y, x)
        self.stack.push(complex_number)


    def handle_digit_input(self, digit):
        """
        Handles digit input, updating the current input and LCD display.

        Args:
            digit (str): A digit character ("0" to "9").
                         Also could be "E" as in 5E-6.
                         Also could be "aHEX"-"fHEX" for 10-15.
                         See input_handler and button_labels
                         
        Returns:
            None
        """
        if (self.input_in_progress and
            digit == b.E and
            b.E in self.current_input):
            return
        if (str(digit).endswith("HEX")):
            digit = digit[0] # fHEX -> f
            config.hexadecimal = True
        if self.input_in_progress:
            self.current_input += digit
        else:
            if self.current_input:
                self.stack.push(float(self.current_input))
                self.current_input = digit
            else:
                if (self.just_pressed_enter):
                    self.stack.pop()
                if (digit == b.E):
                    self.current_input = "1E"
                else:
                    self.current_input = digit
            self.input_in_progress = True

    def add_decimal_point(self):
        """
        Adds a decimal point to the current input.
        
        Returns:
            None
        """
        if self.input_in_progress:
            if "." not in self.current_input:
                self.current_input += "."
        else:
            if self.current_input:
                self.stack.push(float(self.current_input))
            self.current_input = "0."
            self.input_in_progress = True

    def calculate_result(self):
        """
        Finalizes the current input
        Pushes it to the stack
        Updates the LCD display.
        
        Returns:
            None
        """
        self.input_in_progress = False
        if self.current_input:
            try:
                if self.current_input == "1E":
                    self.current_input = "1"
                n = self.current_input
                if (config.hexadecimal):
                    n = int(n, 16)
                self.stack.push(float(n))
                self.stack.push(float(n))
            except ValueError:
                self.current_input = ""
                return
            self.current_input = ""
        elif not self.stack.is_empty():
            self.stack.push(self.stack.peek())
        

    def clear_display(self):
        """
        Empties the stack and clears the input.
        Resets the display to the startup state.
        
        Returns:
            None
        """
        self.stack = Stack()
        self.current_input = ""
        self.input_in_progress = False
        if (config.orient_top_bottom):
            self.lcd.write_at(0, 0, "X: 0" + (" " * (16)))
            self.lcd.write_at(0, 1, "Y: 0" + (" " * (16)))
            self.lcd.write_at(0, 2, "Z: 0" + (" " * (16)))
        else:
            self.lcd.write_at(0, 1, "Z: 0" + (" " * (16)))
            self.lcd.write_at(0, 2, "Y: 0" + (" " * (16)))
            self.lcd.write_at(0, 3, "X: 0" + (" " * (16)))

    def delete_last_input(self):
        """
        Removes the last digit or decimal point if a number is in progress.
        Resets the X row to 0 if the input is one digit or if no input is in progress.
        
        Returns:
            None
        """
        if self.input_in_progress:
            if len(self.current_input) > 1:
                self.current_input = self.current_input[:-1]
            else:
                self.current_input = ""
                self.input_in_progress = False
                self.stack.push(0.0)
        else:
            self.stack.pop()
            self.stack.push(0.0)
        
    def pi(self):
        """
        Adds an approximation of pi to the top of the stack.
        
        Returns:
            None
        """
        self._complete_input()
        self.stack.push(cmath.pi)
        
    def sum_function(self, subtract=False):
        """
        Sums numbers in stack
        
        Args:
            subtract (bool): If True, sum stack.
                             If False, X-Y-Z-...
                             
        Returns:
            None
        """
        if not self.input_in_progress and self.stack.is_empty():
            return
        self._complete_input()
        
        # Temporary list to store the stack's elements (maintaining order)
        temp_stack = []
        while not self.stack.is_empty():
            temp_stack.append(self.stack.pop())
        
        # Reverse temp_stack to match the original stack order: top-to-bottom
        temp_stack = temp_stack[::-1]
        
        # Perform calculation
        if subtract:
            result = temp_stack[-1]  # Start with the top of the stack (first element)
            for value in temp_stack[::-1][1:]:
                result -= value
        else:
            result = sum(temp_stack)  # Simply add all numbers if not subtracting

        # Rebuild the stack with the original elements
        for value in temp_stack[::-1]:
            self.stack.push(value)
        
        # Push the result onto the stack
        self.stack.push(result)
        self.current_input = ""
        self.input_in_progress = False
        
    def split_complex_polar(self):
        """
        Pops top number from stack (or input).
        Pushes Absolute Value then Angle
        
        Returns:
            None
        """
        # unary_operation("Abs")
        if not self.input_in_progress and self.stack.is_empty():
            return
        self._complete_input()
        if self.stack.is_empty():
            x = 0.0
        else:
            x = self.stack.pop()
        result = abs(x)
        self.stack.push(result)
        
        self.stack.push(x)
        self.unary_operation(b.ANGLE)
        
    def split_complex_rect(self):
        """
        Pops top number from stack (or input).
        Pushes Rect then Imag
        
        Returns:
            None
        """
        # unary_operation("Real")
        if not self.input_in_progress and self.stack.is_empty():
            return
        self._complete_input()
        x = self.stack.pop() if not self.stack.is_empty() else 0.0
        if (type(x) == complex):
            result = x.real
        else:
            result = x
        self.stack.push(result)
        
        self.input_in_progress = True
        self.current_input = str(x)
        if (type(x) == complex):
            self.current_input = str(x.real)
            self.calculate_result()
            self.current_input = str(x.imag)
            self.calculate_result()
            self.handle_complex_number()
            
        self.unary_operation(b.IMAG)
        
    def mean(self):
        """
        Calculates the mean of the stack. Pops, not peeks.
        
        Returns:
            None
        """
        self._complete_input()
        n = self.stack.size()
        self.sum_function()
        self.stack.push(float(n))
        self.binary_operation(b.DIVIDE)

    def unary_operation(self, op):
        """
        Performs a unary operation on the top number on the stack.

        Args:
            op (str): A string representing the operation.
                      See input_handler and button_labels for valid ops.
                      
        Returns:
            None
        """
        if not self.input_in_progress and self.stack.is_empty():
            self.stack.push(0.0)
        
        if (op == b.NEGATE) and \
           (self.current_input != "") and \
           (self.current_input[-1] == b.E):
               
            self.current_input += "-"
            return

        self._complete_input()
        
        if (config.degrees and (op == b.TANGENT) and (self.stack.peek() % 180 == 90)) or \
           (not config.degrees and (op == b.TANGENT) and \
            (abs((self.stack.peek() % math.pi) - (math.pi / 2)) < 1e-6)):
            raise UndefinedError("Tan(90 deg) undefined")
        
        if (((op == b.ARCSINE) or (op == b.ARCCOSINE)) and \
            (type(self.stack.peek()) != complex) and \
            ((self.stack.peek() > 1) or (self.stack.peek() < -1))):
            raise UndefinedError("Domain error asin/acos")
        
        if ((op == b.GAMMA) and \
            ((type(self.stack.peek()) == complex) or \
             (self.stack.peek() <= 0))):
            raise UndefinedError("Domain error gamma")
        
        
        
        x = self.stack.pop() if not self.stack.is_empty() else 0.0
        result = None
        
        if (config.degrees and \
            (op == b.SINE or op == b.COSINE or op == b.TANGENT)):
            x = x * math.pi / 180

        if op == b.DEG:
            result = x * 180 / math.pi
        elif op == b.RAD:
            result = x * math.pi / 180
        elif op == b.ROUND:
            if (type(x) == complex):
                re = round(x.real)
                im = round(x.imag)
                result = complex(re, im)
            else:
                result = float(round(x))
        elif op == b.GAMMA:
            if (type(x) != complex):
                result = math.gamma(x)
            else:
                self.stack.push(x)
                return
        elif op == b.NATURAL_LOG:
            if x == 0.0:
                self.stack.push(x)
                return
            if (type(x) == complex):
                result = cmath.log(x)
            elif (x < 0.0):
                result = cmath.log(x)
            else:
                result = math.log(x)
        elif op == b.EXPONENTIAL:
            if (type(x) == complex):
                result = cmath.exp(x)
            else:
                result = math.exp(x)
        elif op == b.LOGARITHM:
            if x == 0.0:
                self.stack.push(x)
                return
            if (type(x) == complex):
                result = cmath.log10(x)            
            elif (x < 0.0):
                result = cmath.log10(x)
            else:
                result = math.log10(x)
        elif op == b.POWER_OF_TEN:
            result = 10**x
        elif op == b.SQUARE:
            result = x**2
        elif op == b.SQRT:
            result = x ** (1/2)
        elif op == b.SINE:
            if (type(x) == complex):
                result = cmath.sin(x)
            else:
                result = math.sin(x)
        elif op == b.COSINE:
            if (type(x) == complex):
                result = cmath.cos(x)
            else:
                result = math.cos(x)
        elif op == b.TANGENT:
            if (type(x) == complex):
                result = cmath.sin(x) / cmath.cos(x)
            else:
                result = math.tan(x)
        elif op == b.ARCSINE:
            if type(x) == complex:
                step1 = (1 - (x ** 2)) ** (1/2)
                step2 = cmath.log(step1 + (x*complex(0,1)))
                result = step2 * complex(0,-1)
            elif (x >= -1 and x <= 1 and
                type(x) != complex):
                result = math.asin(x)
        elif op == b.ARCCOSINE:
            if type(x) == complex:
                step1 = (1 - (x ** 2)) ** (1/2)
                step2 = cmath.log((step1*complex(0,1)) + x)
                result = step2 * complex(0,-1)
            elif (x >= -1 and x <= 1 and
                type(x) != complex):
                result = math.acos(x)
        elif op == b.ARCTANGENT:
            if (type(x) != complex):
                result = math.atan(x)
            else:
                step1 = cmath.log(1 - (complex(0,1)*x))
                step2 = cmath.log(1 + (complex(0,1)*x))
                result = complex(0,1) * (1/2) * (step1 - step2)
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
    
        if (config.degrees and \
            (op == b.ARCSINE or op == b.ARCCOSINE or \
             op == b.ARCTANGENT or op == b.ANGLE)):
            result = result * 180 / math.pi

        if result is not None:
            self.stack.push(result)
            
    def binary_operation(self, op):
        """
        Performs a binary operation on the top two numbers on the stack.

        Args:
            op (str): A string representing the operation.
                      See input_handler and button_labels for valid ops.
                      
        Returns:
            None
        """
        was_in_progress = self.input_in_progress
        self._complete_input()
        
        x = self.stack.pop() if not self.stack.is_empty() else 0.0
        y = self.stack.pop() if not self.stack.is_empty() else 0.0
        if not was_in_progress and \
           op == b.POWER:
            self.stack.push(y)
            
        result = None
            
        if ((op == b.POWER) and \
            (type(x) == complex) and \
            (type(y) == float) and \
            (y == 0.0)):
            self.stack.push(y)
            self.stack.push(x)
            raise UndefinedError("Domain error power")

        if op == b.ADD:
            result = y + x
        elif op == b.SUBTRACT:
            result = y - x
        elif op == b.MULTIPLY:
            result = y * x
        elif op == b.DIVIDE:
            if x == 0:
                self.stack.push(y)
                self.stack.push(x)
            result = y / x
        elif op == b.POWER:
            result = y**x
        elif op == b.SCIENTIFIC_NOTATION:
            result = y * (10**x)
        elif op == b.PERCENT:
            result = y * (x/100)
            self.stack.push(y)
        elif op == b.MODULUS:
            if (type(y) != complex and
                type(x) != complex):
                result = math.fmod(y,x)
            else:
                self.stack.push(x)
                return
        elif op == b.PERMUTATION:
            part1 = math.gamma(y + 1.0)
            part2 = math.gamma(y - x + 1.0)
            result = part1 / part2
        elif op == b.COMBINATION:
            part1 = math.gamma(y + 1)
            part2 = math.gamma(x + 1)
            part3 = math.gamma(y - x + 1)
            result = part1 / (part2 * part3)

        if result is not None:
            self.stack.push(result)

    def swap_values(self):
        """
        Pushes the in-progress number to the stack if any.
        Swaps the two values at the top of the stack and updates the display.
        
        Returns:
            None
        """
        self._complete_input()
        
        if self.stack.size() >= 2:
            x = self.stack.pop()
            y = self.stack.pop()
            self.stack.push(x)
            self.stack.push(y)
            
    def _shorten_format(self, part1, part2):
        """
        Utility function for format_complex_number.
        Given a + bi or a < b, build string!
        
        Args:
            part1 (float): a, either real or abs
            part2 (float): b, either imag or angle
        
        Returns:
            str: String representing the complex number
        """
        max_length = self.lcd.columns - 3
        result = ""
        if abs(part1) < 1e4 and abs(part1) > 1e-4:
            real_part = f"{part1:.4f}".rstrip('0').rstrip('.')
        else:
            if (abs(part1) % 1) == 0:
                real_part = f"{part1}".replace(".0","")
            else:
                real_part = f"{part1:.1e}".replace("+", "")

        if abs(part2) < 1e4 and abs(part2) > 1e-4:
            imag_part = f"{part2:.4f}".rstrip('0').rstrip('.')
        else:
            imag_part = f"{part2:.1e}".replace("+", "")

        if (config.polar):
            if part2 < 0:
                imag_part = imag_part[1:]
                result = f"{real_part} < -{imag_part}"
            else:
                result = f"{real_part} <  {imag_part}"
        else:
            if part2 < 0:
                imag_part = imag_part[1:]
                result = f"{real_part} - j{imag_part}"
            else:
                result = f"{real_part} + j{imag_part}"

        if len(result) > max_length:
            if "e" in real_part:
                real_base, real_exp = real_part.split("e")
                real_part = f"{real_base.split('.')[0]}e{real_exp}"
            if "e" in imag_part:
                imag_base, imag_exp = imag_part.split("e")
                imag_part = f"{imag_base.split('.')[0]}e{imag_exp}"

            if (config.polar):
                if part2 < 0:
                    result = f"{real_part} < -{imag_part}"
                else:
                    result = f"{real_part} <  {imag_part}"
            else:
                if part2 < 0:
                    result = f"{real_part} - j{imag_part}"
                else:
                    result = f"{real_part} + j{imag_part}"
        return result

    def format_complex_number(self, cnum):
        """
        Formats a complex number as a string in rectangular or polar form to fit within the lcd.columns - 3 length.
        
        Args:
            cnum (complex): The complex number to format.
            
        Returns:
            str: The formatted string representing the complex number.
        """
        max_length = 20 - 3
        part1 = cnum.real
        part2 = cnum.imag
        if (config.polar):
            part1 = abs(cnum)
            part2 = math.atan2(cnum.imag, cnum.real)
            if (config.degrees):
                part2 = part2 * 180 / math.pi
        result = self._shorten_format(part1, part2)
        
        result = result[:max_length]
        result += ' ' * (20 - 3 - len(result))
        
        return result
    
    def _complete_input(self):
        """
        The input in progress is now complete. Push to stack!
        
        Returns:
            None
        """
        if self.input_in_progress:
            if self.current_input[-1] == "E":
                self.current_input = self.current_input[:len(self.current_input) - 1]
            n = self.current_input
            if (config.hexadecimal):
                n = int(n, 16)
            self.stack.push(float(n))
            self.current_input = ""
            self.input_in_progress = False
            
    def _get_values(self):
        """
        Retrieve top 3 values from stack
        
        Returns:
            float: number at top of stack
            float: second number on stack
            float: third number on stack
        """
        if self.input_in_progress:
            x_value = self.current_input
            y_value = self.stack.stack[-1] if self.stack.size() > 0 else 0.0000
            z_value = self.stack.stack[-2] if self.stack.size() > 1 else 0.0000
        else:
            x_value = self.stack.peek() if not self.stack.is_empty() else 0.0000
            y_value = self.stack.stack[-2] if self.stack.size() > 1 else 0.0000
            z_value = self.stack.stack[-3] if self.stack.size() > 2 else 0.0000
        return x_value, y_value, z_value
    
    def _get_x_display(self, x_value):
        """
        Build string to display on X row
        
        Args:
            x_value (float/complex): number at top of stack
            
        Returns:
            str: String to display on X row
        """
        if self.input_in_progress:
            if len(x_value) > 20 - 4:  # Adjusting for "..." and "_"
                x_display = "..." + x_value[-(20 - 4):] + "_"
            else:
                x_display = f"X: {x_value}_"
        else:
            if isinstance(x_value, complex):
                # Format complex number for display
                x_display = "X: " + self.format_complex_number(x_value)
            else:
                x_display = f"X: {float(x_value):.8g}"
        x_display += ' ' * (20 - len(x_display))
        return x_display
    
    def _get_x_display_hex(self, x_value):
        """
        Build string to display on X row while config.hexadecimal
        
        Args:
            x_value (float/complex): decimal number at top of stack
        
        Returns:
            str: String to display on X row
        """
        if self.input_in_progress:
            if len(str(x_value)) > 20 - 4:  # Adjusting for "..." and "_"
                x_display = "..." + str(x_value)[-(20 - 4):] + "_"
            else:
                x_display = f"X: {x_value}_"
        else:
            if isinstance(x_value, complex):
                # Format complex number for display
                real_part = hex(round(x_value.real))[2:]
                imag_part = hex(round(x_value.imag))[2:]
                x_display = f"X: {real_part} + {imag_part}i"
            else:
                try:
                    # Format and round decimal values
                    x = hex(round(float(x_value)))[2:]
                    x_display = f"X: {x}"
                except ValueError:
                    x_display = "X: Invalid Input"

        x_display += ' ' * (20 - len(x_display))
        return x_display

    
    def _get_displays(self, y_value, z_value):
        """
        Build strings to display on Y and Z rows
        
        Args:
            y_value (float/complex): second number on stack
            z_value (float/complex): third number on stack
        
        Returns:
            str: String to display on Y row
            str: String to display on Z row
        """
        if isinstance(y_value, complex):
            y_display = "Y: " + self.format_complex_number(y_value)
        else:
            y_display = f"Y: {y_value:.8g}"
        y_display += ' ' * (20 - len(y_display))
        if isinstance(z_value, complex):
            z_display = "Z: " + self.format_complex_number(z_value)
        else:
            z_display = f"Z: {z_value:.8g}"
        z_display += ' ' * (20 - len(z_display))
        return y_display, z_display
    
    def _get_displays_hex(self, y_value, z_value):
        """
        Build strings to display on Y and Z rows in hexadecimal format.
        
        Args:
            y_value (float/complex): second number on stack
            z_value (float/complex): third number on stack
        
        Returns:
            str: String to display on Y row
            str: String to display on Z row
        """
        if isinstance(y_value, complex):
            real_part_y = hex(round(y_value.real))[2:]
            imag_part_y = hex(round(abs(y_value.imag)))[2:]
            plus_or_minus = "+"
            if (y_value.imag < 0):
                plus_or_minus = "-"
            y_display = f"Y: {real_part_y} {plus_or_minus} j{imag_part_y}"
        else:
            try:
                y = hex(round(float(y_value)))[2:]
                y_display = f"Y: {y}"
            except ValueError:
                y_display = "Y: Invalid Input"
        y_display += ' ' * (20 - len(y_display))

        if isinstance(z_value, complex):
            real_part_z = hex(round(z_value.real))[2:]
            imag_part_z = hex(round(abs(z_value.imag)))[2:]
            plus_or_minus = "+"
            if (z_value.imag < 0):
                plus_or_minus = "-"
            z_display = f"Z: {real_part_z} {plus_or_minus} j{imag_part_z}"
        else:
            try:
                z = hex(round(float(z_value)))[2:]
                z_display = f"Z: {z}"
            except ValueError:
                c_display = "Z: Invalid Input"
        z_display += ' ' * (20 - len(z_display))

        return y_display, z_display

    
    def update_display(self):
        """
        Updates the LCD display based on the current state.
        
        Returns:
            None
        """
        x_value, y_value, z_value = self._get_values()
        if (config.hexadecimal):
            x_display = self._get_x_display_hex(x_value)
            y_display, z_display = self._get_displays_hex(y_value, z_value)
        else:
            x_display = self._get_x_display(x_value)
            y_display, z_display = self._get_displays(y_value, z_value)
        
        # Write to the LCD
        if (config.orient_top_bottom):
            self.lcd.write_at(0, 0, x_display)
            self.lcd.write_at(0, 1, y_display)
            self.lcd.write_at(0, 2, z_display)
        else:
            self.lcd.write_at(0, 1, z_display)
            self.lcd.write_at(0, 2, y_display)
            self.lcd.write_at(0, 3, x_display)
        
        if (config.storing or config.recalling):
            if (config.orient_top_bottom):
                row1 = 0
                row2 = 1
            else:
                row1 = 3
                row2 = 2
            self.lcd.write_at(0, row1, " A  B  C  D  E  F   ")
            self.lcd.write_at(0, row2, "Press top row button")
                
