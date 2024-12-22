"""
calc.py
Kobe Goodwin 12/22/2024
Perform operations and keep track of numbers
"""

DECIMAL_PLACES = 5

# Represents a number with DECIMAL_PLACES number of
# decimal places. It has a real and complex part.
# real      absolute value of number left of decimal place
# imag      ... for complex part
# decR      list of digits right of decimal place
# decI      ... for complex part
# negativeR is the real part negative?
# negativeI is the imaginary part negative?
# isDecimal is the number not an integer?
# isComplex is the imaginary part not 0?
class Number:
    def __init__(self, real, imag=0, decR=[], decI=[], negativeR=False, negativeI=False):
        # real and imag are absolute values
        if (real < 0):
            negativeR = True
            real *= -1
        if (imag < 0):
            negativeI = True
            imag *= -1
            
        self.negativeR = negativeR
        self.negativeI = negativeI
        self.real = real
        self.imag = imag
        
        # Copy over decimal places, rest are 0
        self.decR = [0] * DECIMAL_PLACES
        self.decI = [0] * DECIMAL_PLACES
        if (decR == [] and decI == []):
            self.isDecimal = False
        else:
            self.isDecimal = True
        for i in range(0,len(decR)):
            self.decR[i] = decR[i]
        for i in range(0,len(decI)):
            self.decI[i] = decI[i]
            
        # Determine if complex or 0
        if (imag == 0 and self.decI == [0] * DECIMAL_PLACES):
            self.isComplex = False
            self.negativeI = False
        else:
            self.isComplex = True
        if (real == 0 and self.decR == [0] * DECIMAL_PLACES):
            self.negativeR = False
        if (self.decR == [0] * DECIMAL_PLACES and \
            self.decI == [0] * DECIMAL_PLACES):
            self.isDecimal = False




    # You can add Numbers like using "+" operator, ie Number(0) + Number(0)
    def __add__(self, other):
        # Outputs
        real = 0
        imag = 0
        decR = [0] * DECIMAL_PLACES
        decI = [0] * DECIMAL_PLACES
        negativeR = False
        negativeI = False
        
        # Put the negative sign back if need be
        if (self.negativeR):
            selfReal = -1 * self.real
        else:
            selfReal = self.real
        if (self.negativeI):
            selfImag = -1 * self.imag
        else:
            selfImag = self.imag
        if (other.negativeR):
            otherReal = -1 * other.real
        else:
            otherReal = other.real
        if (other.negativeI):
            otherImag = -1 * other.imag
        else:
            otherImag = other.imag
        
        # No complex, no decimal
        if ((not self.isDecimal) and (not other.isDecimal) and
            (not self.isComplex) and (not other.isComplex)):
            real = selfReal + otherReal
            return Number(real)
        # No decimal
        if ((not self.isDecimal) and (not other.isDecimal)):
            real = selfReal + otherReal
            imag = selfImag + otherImag
            return Number(real, imag)
        
        # Subtract larger number from smaller number
        if (greaterThan(self.real,self.decR,\
                        other.real,other.decR)):
            if (self.negativeR != other.negativeR):
                (real, decR, negativeR) = borrowSub(selfReal,\
                        otherReal, self.decR, other.decR, \
                        self.negativeR, negativeR)
        else:
            if (self.negativeR != other.negativeR):
                (real, decR, negativeR) = borrowSub(otherReal,\
                        selfReal,other.decR,self.decR,\
                        other.negativeR, negativeR)
        # Add when the signs are matching
        if (self.negativeR == other.negativeR):
            (real, decR) = carryAdd(selfReal, \
                otherReal, self.decR, other.decR,\
                self.negativeR)
            
        # Repeat for imaginary...
        if (greaterThan(self.imag,self.decI,\
                        other.imag,other.decI)):
            if (self.negativeI != other.negativeI):
                (imag, decI, negativeI) = borrowSub(selfImag,\
                        otherImag, self.decI, other.decI,\
                        self.negativeI, negativeI)
        else:
            if (self.negativeI != other.negativeI):
                (imag, decI, negativeI) = borrowSub(otherImag,\
                        selfImag, other.decI, self.decI,\
                        other.negativeI, negativeI)
        if (self.negativeI == other.negativeI):
            (imag, decI) = carryAdd(selfImag, \
                otherImag, self.decI, other.decI, self.negativeI)
        return Number(real, imag, decR, decI,\
                      negativeR, negativeI)

    # You can subtract Numbers using the "-" operator
    def __sub__(self, other):
        # a - b = a + (-b)
        return self + Number(other.real, other.imag,\
                             other.decR, other.decI,\
                             not other.negativeR,\
                             not other.negativeI)
    
    def __mul__(self, other):
        pass
    
    def __truediv__(self, other):
        pass
    
    def __mod__(self, other):
        pass
    
    def __pow__(self, other):
        pass
    
    def __str__(self):
        if (self.negativeR):
            a = "-" + str(self.real)
        else:
            a = str(self.real)
        if (self.negativeI):
            b = " - j" + str(self.imag)
        else:
            b = " + j" + str(self.imag)
        if ((not self.isDecimal) and (not self.isComplex)):
            return a
        if ((not self.isDecimal) and self.isComplex):
            return a + b
        r = ""
        i = ""
        for x in range(0,DECIMAL_PLACES):
            r += str(self.decR[x])
            i += str(self.decI[x])
        
        if (not self.isComplex):
            return a + "." + r
        
        return a + "." + r + b + "." + i

        

stack = []

def getX():
    if (len(stack) > 0):
        return stack[-1]
    else:
        return Number(0)

def getY():
    if (len(stack) > 1):
        return stack[-2]
    else:
        return Number(0)
    
def carryAdd(xReIm, yReIm, xDeci, yDeci,\
             negativeCondition):
    carry = 0
    zDeci = [0] * DECIMAL_PLACES
    for i in range(DECIMAL_PLACES - 1,-1,-1):
        t = carry + xDeci[i] + yDeci[i]
        if (t > 9):
            carry = 1
            t -= 10
        else:
            carry = 0
        zDeci[i] = t
    if (negativeCondition):
        zReIm = xReIm + yReIm - carry
    else:
        zReIm = xReIm + yReIm + carry
    return (zReIm, zDeci)

def borrowSub(xReIm, yReIm, xDeci, yDeci,\
              negativeCondition, negativeOutput):
    borrow = 0
    zDeci = [0] * DECIMAL_PLACES
    for i in range(DECIMAL_PLACES - 1,-1,-1):
        t = borrow + xDeci[i] - yDeci[i]
        if (t < 0):
            borrow = -1
            t += 10
        else:
            borrow = 0
        zDeci[i] = t
    if (negativeCondition):
        real = xReIm + yReIm - borrow
    else:
        real = xReIm + yReIm + borrow
    if (real == 0 and negativeCondition):
        negativeOutput = True
    return (real, zDeci, negativeOutput)
    
# Compare two Numbers > 0
def greaterThan(n1, d1, n2, d2):
    if (n1 > n2):
        return True
    if (n2 > n1):
        return False
    for x in range(0,len(d1)):
        if d1[x] > d2[x]:
            return True
        if d2[x] > d1[x]:
            return False
    return False

# 1.12345 + j2.98765
# 3.85762 + j1.42738
x = Number(1,2,[1,2,3,4,5],[9,8,7,6,5])
y = Number(3,1,[8,5,7,6,2],[4,2,7,3,8])
if (str(x + y) == "4.98107 + j4.41503"):
    print("Test 1 Success!")
else:
    print("Test 1 Failed!")
    print(x+y)
#  4.56789 - j1.12345
# -3.98765 - j2.24567
#  0.58024 - j3.36912
x = Number(4,-1,[5,6,7,8,9],[1,2,3,4,5])
y = Number(-3,-2,[9,8,7,6,5],[2,4,5,6,7])
if (str(x + y) == "0.58024 - j3.36912"):
    print("Test 2 Success!")
else:
    print("Test 2 Failed!")
    print(x+y)
# -1.12345 + j3.56789
# -2.24567 - j3.69134
x = Number(-1,3,[1,2,3,4,5],[5,6,7,8,9])
y = Number(-2,-3,[2,4,5,6,7],[6,9,1,3,4])
if (str(x + y) == "-3.36912 - j0.12345"):
    print("Test 3 Success!")
else:
    print("Test 3 Failed!")
    print(x+y)
#  4.56789 - j4.56789
# -3.98765 + j3.98765
#  0.58024 - j0.58024
x = Number(4,-4,[5,6,7,8,9],[5,6,7,8,9])
y = Number(-3,3,[9,8,7,6,5],[9,8,7,6,5])
if (str(x + y) == "0.58024 - j0.58024"):
    print("Test 4 Success!")
else:
    print("Test 4 Failed!")
    print(x+y)
# -0.21871 + j7.85248
# -1.17705 + j7.56405
# -1.39576 + j15.41653
x = Number(0,7,[2,1,8,7,1],[8,5,2,4,8],True)
y = Number(-1,7,[1,7,7,0,5],[5,6,4,0,5])
if (str(x + y) == "-1.39576 + j15.41653"):
    print("Test 5 Success!")
else:
    print("Test 5 Failed!")
    print(x+y)
#  6.16572 + j3.35165
# -3.13915 - j3.58105
#  3.02657 - j0.22940
x = Number(6,3,[1,6,5,7,2],[3,5,1,6,5])
y = Number(-3,-3,[1,3,9,1,5],[5,8,1,0,5])
if (str(x + y) == "3.02657 - j0.22940"):
    print("Test 6 Success!")
else:
    print("Test 6 Failed!")
    print(x+y)
#  8.00090 - j6.48097
# -4.35450 + j6.51657
#  3.64640 + j0.09560
x = Number(8,-6,[0,0,0,9,0],[4,8,0,9,7])
y = Number(-4,6,[3,5,4,5,0],[5,1,6,5,7])
if (str(x + y) == "3.64640 + j0.03560"):
    print("Test 7 Success!")
else:
    print("Test 7 Failed!")
    print(x+y)
# -8.78151 - j9.45470
#  8.78151 + j9.45470
x = Number(-8,-9,[7,8,1,5,1],[4,5,4,7,0])
y = Number(8,9,[7,8,1,5,1],[4,5,4,7,0])
if (str(x + y) == "0"):
    print("Test 8 Success!")
else:
    print("Test 8 Failed!")
    print(x+y)
#   -0.21871 + j7.85248
# -(-1.17705 + j7.56405)
#    0.95834 + j0.28843
x = Number(0,7,[2,1,8,7,1],[8,5,2,4,8],True)
y = Number(-1,7,[1,7,7,0,5],[5,6,4,0,5])
if (str(x - y) == "0.95834 + j0.28843"):
    print("Test 9 Success!")
else:
    print("Test 9 Failed!")
    print(x-y)
#  -3.74827 - j5.59348
# + 6.74784 + j2.16946
#   2.99957 - j3.42402
x = Number(-3,-5,[7,4,8,2,7],[5,9,3,4,8])
y = Number(6,2,[7,4,7,8,4],[1,6,9,4,6])
if (str(x + y) == "2.99957 - j3.42402"):
    print("Test 10 Success!")
else:
    print("Test 10 Failed!")
    print(x+y)
#   -1.97606 - j1.76830
# +  5.85972 - j2.87998
#    3.88366 - j4.64828
x = Number(-1,-1,[9,7,6,0,6],[7,6,8,3,0])
y = Number(5,-2,[8,5,9,7,2],[8,7,9,9,8])
if (str(x + y) == "3.88366 - j4.64828"):
    print("Test 11 Success!")
else:
    print("Test 11 Failed!")
    print(x+y)
#   -7.86073 - j2.40720
# -(-9.33898 - j0.50713)
#    1.47825 - j1.90007
x = Number(-7,-2,[8,6,0,7,3],[4,0,7,2,0])
y = Number(-9,0,[3,3,8,9,8],[5,0,7,1,3],True,True)
if (str(x - y) == "1.47825 - j1.90007"):
    print("Test 12 Success!")
else:
    print("Test 12 Failed!")
    print(x-y)
#    9.08207 - j4.70485
# -( 1.41368 + j1.95772)
#    7.66839 - j6.66257
x = Number(9,-4,[0,8,2,0,7],[7,0,4,8,5])
y = Number(1,1,[4,1,3,6,8],[9,5,7,7,2])
if (str(x - y) == "7.66839 - j6.66257"):
    print("Test 13 Success!")
else:
    print("Test 13 Failed!")
    print(x-y)
#    9.67690 + j7.62533
# -( 6.25989 - j2.75773)
#    3.41701 + j10.38306
x = Number(9,7,[6,7,6,9,0],[6,2,5,3,3])
y = Number(6,-2,[2,5,9,8,9],[7,5,7,7,3])
if (str(x - y) == "3.41701 + j10.38306"):
    print("Test 14 Success!")
else:
    print("Test 14 Failed!")
    print(x-y)
#   -7.51023 - j5.59336
# -( 4.89429 - j0.80114)
#  -12.40452 - j4.79222
x = Number(-7,-5,[5,1,0,2,3],[5,9,3,3,6])
y = Number(4,0,[8,9,4,2,9],[8,0,1,1,4],False,True)
z = x - y
if (str(z) == "-12.40452 - j4.79222"):
    print("Test 15 Success!")
else:
    print("Test 15 Failed!")
    print(z)

#   -4.39372 - j2.57503
# -( 7.73770 - j2.87012)
#  -12.13142 + j0.29509
x = Number(-4,-2,[3,9,3,7,2],[5,7,5,0,3])
y = Number(7,-2,[7,3,7,7,0],[8,7,0,1,2])
if (str(x - y) == "-12.13142 + j0.29509"):
    print("Test 16 Success!")
else:
    print("Test 16 Failed!")
    print(x-y)
#    5 + j2
# -(-2 + j5)
#    7 - j3
x = Number(5,2)
y = Number(-2,5)
if (str(x-y) == "7 - j3"):
    print("Test 17 Success!")
else:
    print("Test 17 Failed!")
    print(x-y)
# 0-0=0
x = Number(0)
y = Number(0)
if (str(x-y) == "0"):
    print("Test 18 Success!")
else:
    print("Test 18 Failed!")
    print(x-y)
#   -8.00608 - j7.33551
# -(-0.75162 - j8.77572)
#   -7.25446 + j1.44021
x = Number(-8,-7,[0,0,6,0,8],[3,3,5,5,1])
y = Number(0,-8,[7,5,1,6,2],[7,7,5,7,2],True)
if (str(x-y) == "-7.25446 + j1.44021"):
    print("Test 19 Success!")
else:
    print("Test 19 Failed!")
    print(x-y)
#   -1.02188 + j5.98383
# -( 5.48416 - j9.46274)
#   -6.50604 + j15.44655
x = Number(-1,5,[0,2,1,8,8],[9,8,3,8,3])
y = Number(5,-9,[4,8,4,1,6],[4,6,2,7,4])
if (str(x-y) == "-6.50604 + j15.44657"):
    print("Test 20 Success!")
else:
    print("Test 20 Failed!")
    print(x-y)