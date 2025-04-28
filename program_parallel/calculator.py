"""
calculator.py
Kobe Goodwin
4/28/2025

Keeps track of the stack and user input.
Displays new output to screen.
"""

import math
import cmath
from stack import Stack
from button_labels import ButtonLabels as b
import config

class CustomError(Exception):
    pass

class UndefinedError(CustomError):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

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
        self.store = None
        self.just_pressed_enter= False

        # Initialize LCD display
        if (config.orient_top_bottom):
            self.lcd.write_at(0, 0, "A: 0")
            self.lcd.write_at(0, 1, "B: 0")
            self.lcd.write_at(0, 2, "C: 0")
        else:
            self.lcd.write_at(0, 1, "C: 0")
            self.lcd.write_at(0, 2, "B: 0")
            self.lcd.write_at(0, 3, "A: 0")
        
    def roll(self):
        """
        Roll stack down: A to bottom, B to top
        """
        self._complete_input()
        if (self.stack.is_empty()):
            return
        self.stack = self.stack + self.stack.pop()
        
    def store_number(self):
        """
        Store the top register
        """
        self._complete_input()
        if (not self.stack.is_empty()):
            self.store = self.stack.peek()
            if (config.orient_top_bottom):
                self.lcd.write_at(10, self.lcd_rows - 3, "Stored")
            else:
                self.lcd.write_at(10, self.lcd.rows - 1, "Stored")
        
    def recall_number(self):
        """
        Recall the stored value
        """
        if (self.store):
            self._complete_input()
            self.stack.push(self.store)

    def handle_complex_number(self, polar = False):
        """
        Handles complex number input by creating a complex number from the
        top two numbers on the stack and updates the display.
        
        Args:
        polar (bool): True for interpreting Y<X. False for Y+jX
        """
        
        if self.stack.size() == 0:
            self.stack.push(0.0)
        
        self._complete_input()

        x = self.stack.pop()
        y = self.stack.peek()
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
                         Also could be "AHEX"-"FHEX" for 10-15.
        """
        if (self.input_in_progress and
            digit == b.E and
            b.E in self.current_input):
            return
        if (str(digit).endswith("HEX")):
            digit = digit[0]
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
        Finalizes the current input, pushes it to the stack, and updates
        the LCD display.
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
        Empties the stack and clears the input. Resets the display to the startup state.
        """
        self.stack = Stack()
        self.current_input = ""
        self.input_in_progress = False
        if (config.orient_top_bottom):
            self.lcd.write_at(0, self.lcd.rows - 2, "A: 0" + (" " * (self.lcd.columns - 4)))
            self.lcd.write_at(0, self.lcd.rows - 1, "B: 0" + (" " * (self.lcd.columns - 4)))
            self.lcd.write_at(0, self.lcd.rows - 0, "C: 0" + (" " * (self.lcd.columns - 4)))
        else:
            self.lcd.write_at(0, self.lcd.rows - 3, "C: 0" + (" " * (self.lcd.columns - 4)))
            self.lcd.write_at(0, self.lcd.rows - 2, "B: 0" + (" " * (self.lcd.columns - 4)))
            self.lcd.write_at(0, self.lcd.rows - 1, "A: 0" + (" " * (self.lcd.columns - 4)))
        if (config.orient_top_bottom):
            self.lcd.write_at(0, 0, "A: 0" + (" " * (self.lcd.columns - 4)))
            self.lcd.write_at(0, 1, "B: 0" + (" " * (self.lcd.columns - 4)))
            self.lcd.write_at(0, 2, "C: 0" + (" " * (self.lcd.columns - 4)))
        else:
            self.lcd.write_at(0, 1, "C: 0" + (" " * (self.lcd.columns - 4)))
            self.lcd.write_at(0, 2, "B: 0" + (" " * (self.lcd.columns - 4)))
            self.lcd.write_at(0, 3, "A: 0" + (" " * (self.lcd.columns - 4)))

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
                self.stack.push(0.0)
        else:
            self.stack.pop()
            self.stack.push(0.0)
        
    def pi(self):
        """
        Adds an approximation of pi to the top of the stack.
        """
        self._complete_input()
        self.stack.push(cmath.pi)
        
    def sum_function(self, subtract=False):
        """
        Sums numbers in stack
        """
        if not self.input_in_progress and self.stack.is_empty():
            return
        self._complete_input()
        list_stack = []
        while (not self.stack.is_empty()):
            list_stack += [self.stack.pop()]
        result = list_stack[-1]
        for i in range(0,len(list_stack)-1):
            if subtract:
                result -= list_stack[i]
            else:
                result += list_stack[i]
        self.stack.push(result)
        self.current_input = ""
        self.input_in_progress = False
        
    def split_complex_polar(self):
        """
        Pops top number from stack (or input).
        Pushes Absolute Value then Angle
        """
        # unary_operation("Abs")
        if not self.input_in_progress and self.stack.is_empty():
            return
        self._complete_input()
        x = self.stack.pop() if not self.stack.is_empty() else 0.0
        result = abs(x)
        self.stack.push(result)
        
        # Get x to the top of the stack
        self.input_in_progress = True
        self.current_input = str(x)
        if (type(x) == complex):
            self.current_input = str(x.real)
            self.calculate_result()
            self.current_input = str(x.imag)
            self.calculate_result()
            self.handle_complex_number()
            
        self.unary_operation(b.ANGLE)
        
        if (config.degrees):
            n = self.stack.pop()
            n = n * 180 / math.pi
            self.stack.push(n)
        
    def split_complex_rect(self):
        """
        Pops top number from stack (or input).
        Pushes Rect then Imag
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
        
        # Get x to the top of the stack
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
                      Valid operations are: "Natural Log", "Exponential", "Logarithm",
                      "Power of Ten", "Square", "Sine", "Cosine", "Tangent",
                      "Arcsine", "Arccosine", "Arctangent", "Negate", "Reciprocal",
                      "Conjugate", "Sqrt", "Abs", "Angle", "Real", "Imag", 
                      "Deg", "Rad", "Round", "Gamma"
        """
        if not self.input_in_progress and self.stack.is_empty():
            self.stack.push(0.0)
        
        if (op == b.NEGATE) and \
           (self.current_input != "") and \
           (self.current_input[-1] == b.E):
               
            self.current_input += "-"
            return

        self._complete_input()
        
        if (((op == b.ARCSINE) or (op == b.ARCCOSINE)) and \
            ((type(self.stack.peek()) is complex))):
            raise UndefinedError("Domain error asin/acos")
        
        if (config.degrees and (op == b.TANGENT) and (self.stack.peek() % 180 == 90)) or \
           (not config.degrees and (op == b.TANGENT) and \
            (abs((self.stack.peek() % math.pi) - (math.pi / 2)) < 1e-6)):
            raise UndefinedError("Tan(90 deg) undefined")
        
        if (((op == b.ARCSINE) or (op == b.ARCCOSINE)) and \
            ((self.stack.peek() > 1) or (self.stack.peek() < -1))):
            raise UndefinedError("Domain error asin/acos")
        
        if ((type(self.stack.peek()) == complex or \
            self.stack.peek() <= 0) and
            (op == b.GAMMA)):
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
            if (x >= -1 and x <= 1 and
                type(x) != complex):
                result = math.asin(x)
            elif type(x) == complex:
                step1 = (1 - (x ** 2)) ** (1/2)
                step2 = cmath.log(step1 + (x*complex(0,1)))
                result = step2 * complex(0,-1)
        elif op == b.ARCCOSINE:
            if (x >= -1 and x <= 1 and
                type(x) != complex):
                result = math.acos(x)
            elif type(x) == complex:
                step1 = (1 - (x ** 2)) ** (1/2)
                step2 = cmath.log((step1*complex(0,1)) + x)
                result = step2 * complex(0,-1)
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
            (op == b.ARCSINE or op == b.ARCCOSINE or op == b.ARCTANGENT)):
            result = result * 180 / math.pi

        if result is not None:
            self.stack.push(result)
            
    def binary_operation(self, op):
        """
        Performs a binary operation on the top two numbers on the stack.

        Args:
            op (str): A string representing the operation.
                      Valid operations are: "Add", "Subtract", "Multiply", "Divide", "Power", "Scientific Notation"
                      "Percent", "Modulus"
        """
        was_in_progress = self.input_in_progress
        self._complete_input()
        
        x = self.stack.pop() if not self.stack.is_empty() else 0.0
        y = self.stack.pop() if not self.stack.is_empty() else 0.0
        if not was_in_progress and \
           op == b.POWER:
            self.stack.push(y)
        
        #self.stack.pop()
        
        result = None

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
            #self.stack.push(y)
            result = y**x
        elif op == b.SCIENTIFIC_NOTATION:
            result = y * (10**x)
        elif op == b.PERCENT:
            result = y / (100*x)
            self.stack.push(y)
        elif op == b.MODULUS:
            if (type(y) != complex and
                type(x) != complex):
                result = math.fmod(y,x)
            else:
                self.stack.push(x)
                return

        if result is not None:
            self.stack.push(result)

    def swap_values(self):
        """
        Pushes the in-progress number to the stack if any.
        Swaps the two values at the top of the stack and updates the display.
        """
        self._complete_input()
        
        if self.stack.size() >= 2:
            x = self.stack.pop()
            y = self.stack.pop()
            self.stack.push(x)
            self.stack.push(y)
            
    def _shorten_format(self, part1, part2):
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

        # Construct the full string in rectangular form
        if (config.polar):
            if part2 < 0:
                imag_part = imag_part[1:]  # Remove the negative sign in the imaginary part
                result = f"{real_part} < -{imag_part}"
            else:
                result = f"{real_part} <  {imag_part}"
        else:
            if part2 < 0:
                imag_part = imag_part[1:]  # Remove the negative sign in the imaginary part
                result = f"{real_part} - j{imag_part}"
            else:
                result = f"{real_part} + j{imag_part}"

        # Ensure the result fits within max_length
        if len(result) > max_length:
            # Modify to truncate decimal point and digits after it in scientific notation
            if "e" in real_part:
                real_base, real_exp = real_part.split("e")
                real_part = f"{real_base.split('.')[0]}e{real_exp}"
            if "e" in imag_part:
                imag_base, imag_exp = imag_part.split("e")
                imag_part = f"{imag_base.split('.')[0]}e{imag_exp}"

            # Reconstruct the result after truncation
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
        max_length = self.lcd.columns - 3
        part1 = cnum.real
        part2 = cnum.imag
        if (config.polar):
            part1 = abs(cnum)
            part2 = math.atan2(cnum.imag, cnum.real)
            if (config.degrees):
                part2 = part2 * 180 / math.pi
        result = self._shorten_format(part1, part2)
        
        result = result[:max_length]
        result += ' ' * (self.lcd.columns - 3 - len(result))
        
        return result
    
    def _complete_input(self):
        """
        The input in progress is now complete. Push to stack!
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
        """
        if self.input_in_progress:
            a_value = self.current_input
            b_value = self.stack.stack[-1] if self.stack.size() > 0 else 0.0000
            c_value = self.stack.stack[-2] if self.stack.size() > 1 else 0.0000
        else:
            a_value = self.stack.peek() if not self.stack.is_empty() else 0.0000
            b_value = self.stack.stack[-2] if self.stack.size() > 1 else 0.0000
            c_value = self.stack.stack[-3] if self.stack.size() > 2 else 0.0000
        return a_value, b_value, c_value
    
    def _get_a_display(self, a_value):
        """
        Build string to display on A row
        """
        if self.input_in_progress:
            if len(a_value) > self.lcd.columns - 4:  # Adjusting for "..." and "_"
                a_display = "..." + a_value[-(self.lcd.columns - 4):] + "_"
            else:
                a_display = f"A: {a_value}_"
        else:
            if isinstance(a_value, complex):
                # Format complex number for display
                a_display = "A: " + self.format_complex_number(a_value)
            else:
                a_display = f"A: {float(a_value):.8g}"
        a_display += ' ' * (self.lcd.columns - len(a_display))
        return a_display
    
    def _get_a_display_hex(self, a_value):
        """
        Build string to display on A row while config.hexadecimal
        """
        def format_as_hex(value):
            """Helper to convert and format numbers as hexadecimal."""
            try:
                return hex(round(value))[2:]
            except TypeError:
                return "Invalid"

        if self.input_in_progress:
            if len(str(a_value)) > self.lcd.columns - 4:  # Adjusting for "..." and "_"
                a_display = "..." + str(a_value)[-(self.lcd.columns - 4):] + "_"
            else:
                a_display = f"A: {a_value}_"
        else:
            if isinstance(a_value, complex):
                # Format complex number for display
                real_part = format_as_hex(a_value.real)
                imag_part = format_as_hex(a_value.imag)
                a_display = f"A: {real_part} + {imag_part}i"
            else:
                try:
                    # Format and round decimal values
                    a_display = f"A: {format_as_hex(float(a_value))}"
                except ValueError:
                    a_display = "A: Invalid Input"

        a_display += ' ' * (self.lcd.columns - len(a_display))
        return a_display

    
    def _get_displays(self, b_value, c_value):
        """
        Build strings to display on B and C rows
        """
        if isinstance(b_value, complex):
            # Format complex number for display
            b_display = "B: " + self.format_complex_number(b_value)
        else:
            b_display = f"B: {b_value:.8g}"  # Use general format for large/small numbers
        b_display += ' ' * (self.lcd.columns - len(b_display))
        if isinstance(c_value, complex):
            # Format complex number for display
            c_display = "C: " + self.format_complex_number(c_value)
        else:
            c_display = f"C: {c_value:.8g}"  # Use general format for large/small numbers
        c_display += ' ' * (self.lcd.columns - len(c_display))
        return b_display, c_display
    
    def _get_displays_hex(self, b_value, c_value):
        """
        Build strings to display on B and C rows in hexadecimal format.
        """
        def format_as_hex(value):
            """Helper to convert and format numbers as hexadecimal."""
            try:
                return hex(round(value))[2:]
            except TypeError:
                return "Invalid"

        if isinstance(b_value, complex):
            # Format complex number for display
            real_part_b = format_as_hex(b_value.real)
            imag_part_b = format_as_hex(b_value.imag)
            b_display = f"B: {real_part_b} + {imag_part_b}i"
        else:
            try:
                # Format and round decimal values
                b_display = f"B: {format_as_hex(float(b_value))}"
            except ValueError:
                b_display = "B: Invalid Input"
        b_display += ' ' * (self.lcd.columns - len(b_display))

        if isinstance(c_value, complex):
            # Format complex number for display
            real_part_c = format_as_hex(c_value.real)
            imag_part_c = format_as_hex(c_value.imag)
            c_display = f"C: {real_part_c} + {imag_part_c}i"
        else:
            try:
                # Format and round decimal values
                c_display = f"C: {format_as_hex(float(c_value))}"
            except ValueError:
                c_display = "C: Invalid Input"
        c_display += ' ' * (self.lcd.columns - len(c_display))

        return b_display, c_display

    
    def update_display(self):
        """
        Updates the LCD display based on the current state.
        """
        a_value, b_value, c_value = self._get_values()
        if (config.hexadecimal):
            a_display = self._get_a_display_hex(a_value)
            b_display, c_display = self._get_displays_hex(b_value, c_value)
        else:
            a_display = self._get_a_display(a_value)
            b_display, c_display = self._get_displays(b_value, c_value)
        
        # Write to the LCD
        if (config.orient_top_bottom):
            self.lcd.write_at(0, 0, a_display)
            self.lcd.write_at(0, 1, b_display)
            self.lcd.write_at(0, 2, c_display)
        else:
            self.lcd.write_at(0, 1, c_display)
            self.lcd.write_at(0, 2, b_display)
            self.lcd.write_at(0, 3, a_display)







