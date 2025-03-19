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
        self.store = None

        # Initialize LCD display
        if (self.lcd.rows == 4):
            self.lcd.write_at(0, lcd.rows - 4, "D: 0")
            self.lcd.write_at(0, lcd.rows - 3, "C: 0")
        self.lcd.write_at(0, lcd.rows - 2, "B: 0")
        self.lcd.write_at(0, lcd.rows - 1, "A: 0")
        
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
        self._complete_input()
        
        if self.stack.size() < 2:
            return

        x = self.stack.pop()
        y = self.stack.pop()
        if (polar):
            if (type(x) == complex):
                real = y * cmath.cos(x*math.pi/180)
            else:
                real = y * math.cos(x*math.pi/180)
            if (type(y) == complex):
                imag = y * cmath.sin(x*math.pi/180)
            else:
                imag = y * math.sin(x*math.pi/180)
            complex_number = complex(real, imag)
            print(real)
            print(imag)
        else:
            complex_number = complex(y, x)
        self.stack.push(complex_number)


    def handle_digit_input(self, digit):
        """
        Handles digit input, updating the current input and LCD display.

        Args:
            digit (str): A digit character ("0" to "9").
        """
        if (self.input_in_progress and
            digit == b.E and
            b.E in self.current_input):
            return
        if self.input_in_progress:
            self.current_input += digit
        else:
            if self.current_input:
                self.stack.push(float(self.current_input))
                self.current_input = digit
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
        if self.current_input:
            try:
                self.stack.push(float(self.current_input))
            except ValueError:
                self.current_input = ""
                return
            self.current_input = ""
        elif not self.stack.is_empty():
            self.stack.push(self.stack.peek())
        
        self.input_in_progress = False

    def clear_display(self):
        """
        Empties the stack and clears the input. Resets the display to the startup state.
        """
        self.stack = Stack()
        self.current_input = ""
        self.input_in_progress = False
        if (self.lcd.rows == 4):
            self.lcd.write_at(0, self.lcd.rows - 4, "D: 0" + (" " * (self.lcd.columns - 4)))
            self.lcd.write_at(0, self.lcd.rows - 3, "C: 0" + (" " * (self.lcd.columns - 4)))
        self.lcd.write_at(0, self.lcd.rows - 2, "B: 0" + (" " * (self.lcd.columns - 4)))
        self.lcd.write_at(0, self.lcd.rows - 1, "A: 0" + (" " * (self.lcd.columns - 4)))

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
        
    def pi(self):
        """
        Adds an approximation of pi to the top of the stack.
        """
        self.calculate_result()
        self.current_input = str(cmath.pi)
        self.calculate_result()
        
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
        result = list_stack[0]
        for i in range(1,len(list_stack)):
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

    def unary_operation(self, op):
        """
        Performs a unary operation on the top number on the stack.

        Args:
            op (str): A string representing the operation.
                      Valid operations are: "Natural Log", "Exponential", "Logarithm",
                      "Power of Ten", "Square", "Sine", "Cosine", "Tangent",
                      "Arcsine", "Arccosine", "Arctangent", "Negate", "Reciprocal",
                      "Conjugate", "Sqrt", "Abs", "Angle", "Real", "Imag"
        """
        if not self.input_in_progress and self.stack.is_empty():
            return
        
        if (op == b.NEGATE) and \
           (self.current_input != "") and \
           (self.current_input[-1] == b.E):
               
            self.current_input += "-"
            return

        self._complete_input()
        
        x = self.stack.pop() if not self.stack.is_empty() else 0.0
        result = None

        if op == b.NATURAL_LOG:
            if x == 0.0:
                self.stack.push(x)
                return
            if (type(x) == complex):
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

        if result is not None:
            self.stack.push(result)
            
    def binary_operation(self, op):
        """
        Performs a binary operation on the top two numbers on the stack.

        Args:
            op (str): A string representing the operation.
                      Valid operations are: "Add", "Subtract", "Multiply", "Divide", "Power", "Scientific Notation".
        """
        self._complete_input()
        
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
    
    def format_complex_number(self, cnum):
        """
        Formats a complex number as a string in rectangular form to fit within the lcd.columns - 3 length.
        
        Args:
            cnum (complex): The complex number to format.
            
        Returns:
            str: The formatted string representing the complex number.
        """
        max_length = self.lcd.columns - 3
        
        # Format real and imaginary parts
        if abs(cnum.real) < 1e4 and abs(cnum.real) > 1e-4:
            real_part = f"{cnum.real:.4f}".rstrip('0').rstrip('.')
        else:
            real_part = f"{cnum.real:.1e}".replace("+", "")
        
        if abs(cnum.imag) < 1e4 and abs(cnum.imag) > 1e-4:
            imag_part = f"{cnum.imag:.4f}".rstrip('0').rstrip('.')
        else:
            imag_part = f"{cnum.imag:.1e}".replace("+", "")
        
        # Construct the full string
        if cnum.imag < 0:
            imag_part = imag_part[1:]
            result = f"{real_part} - j{imag_part}"
        else:
            result = f"{real_part} + j{imag_part}"
        
        # Truncate to fit within max_length
        if len(result) > max_length:
            if abs(cnum.real) < 1e4 and abs(cnum.real) > 1e-4:
                truncated_real = f"{cnum.real:.1f}".rstrip('0').rstrip('.')
            else:
                truncated_real = f"{cnum.real:.1e}".replace("+", "")
            
            if abs(cnum.imag) < 1e4 and abs(cnum.imag) > 1e-4:
                truncated_imag = f"{cnum.imag:.1f}".rstrip('0').rstrip('.')
            else:
                truncated_imag = f"{cnum.imag:.1e}".replace("+", "")
            
            if cnum.imag < 0:
                truncated_imag = truncated_imag[1:]
                result = f"{truncated_real}-j{truncated_imag}"
            else:
                result = f"{truncated_real}+j{truncated_imag}"
        
        result = result[:max_length]
        result += ' ' * (self.lcd.columns - 3 - len(result))
        
        return result 
    
    
    def _complete_input(self):
        if self.input_in_progress:
            self.stack.push(float(self.current_input))
            self.current_input = ""
            self.input_in_progress = False
    
    def update_display(self):
        """
        Updates the LCD display based on the current state.
        """
        if self.input_in_progress:
            a_value = self.current_input
            if len(a_value) > self.lcd.columns - 4:  # Adjusting for "..." and "_"
                a_display = "..." + a_value[-(self.lcd.columns - 4):] + "_"
            else:
                a_display = f"A: {a_value}_"
            b_value = self.stack.stack[-1] if self.stack.size() > 0 else 0.0000
            c_value = self.stack.stack[-2] if self.stack.size() > 1 else 0.0000
            d_value = self.stack.stack[-3] if self.stack.size() > 2 else 0.0000
        else:
            a_value = self.stack.peek() if not self.stack.is_empty() else "0.0000"
            if isinstance(a_value, complex):
                # Format complex number for display
                a_display = "A: " + self.format_complex_number(a_value)
            else:
                a_display = f"A: {float(a_value):.4g}"  # Use general format for large/small numbers
            b_value = self.stack.stack[-2] if self.stack.size() > 1 else 0.0000
            c_value = self.stack.stack[-3] if self.stack.size() > 2 else 0.0000
            d_value = self.stack.stack[-4] if self.stack.size() > 3 else 0.0000

        if isinstance(b_value, complex):
            # Format complex number for display
            b_display = "B: " + self.format_complex_number(b_value)
        else:
            b_display = f"B: {b_value:.4g}"  # Use general format for large/small numbers
            b_display += ' ' * (self.lcd.columns - len(b_display))
        if isinstance(c_value, complex):
            # Format complex number for display
            c_display = "C: " + self.format_complex_number(c_value)
        else:
            c_display = f"C: {c_value:.4g}"  # Use general format for large/small numbers
            c_display += ' ' * (self.lcd.columns - len(c_display))
        if isinstance(d_value, complex):
            # Format complex number for display
            d_display = "D: " + self.format_complex_number(d_value)
        else:
            d_display = f"D: {d_value:.4g}"  # Use general format for large/small numbers
            d_display += ' ' * (self.lcd.columns - len(d_display))

        a_display += ' ' * (self.lcd.columns - len(a_display))
        
        
        # Write to the LCD
        if (self.lcd.rows == 4):
            self.lcd.write_at(0, self.lcd.rows - 4, d_display)
            self.lcd.write_at(0, self.lcd.rows - 3, c_display)
        self.lcd.write_at(0, self.lcd.rows - 2, b_display)
        self.lcd.write_at(0, self.lcd.rows - 1, a_display)






