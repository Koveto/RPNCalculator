"""
number.py
Kobe Goodwin 12/31/2024
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
    
    # You can divide Numbers using the "/" operator
    def __truediv__(self, other):
        """print("Divide")
        print(self)
        print(other)
        print()"""
        # self = a + bi
        # other = c + di
        # 1. find c^2 + d^2
        
        if ((not self.isComplex) and (not other.isComplex)):
            # a/c
            (a, b, c) = longDivision(self.real, other.real,\
                self.decR, other.decR,\
                self.negativeR, other.negativeR)
            """print("NEITHER COMPLEX")
            print((a,b,c))
            print()"""
            return Number(a, 0, b, [0] * DECIMAL_PLACES, c, False)
        
        # 1/c
        (s1ReIm, s1Deci, s1Neg) = longDivision(1,other.real,\
                [0] * DECIMAL_PLACES, other.decR,\
                False, other.negativeR)
        # c^2 = c/s1
        (s2ReIm, s2Deci, s2Neg) = longDivision(other.real, s1ReIm,\
                other.decR, s1Deci,\
                other.negativeR, s1Neg)
        # 1/d
        (s3ReIm, s3Deci, s3Neg) = longDivision(1,other.imag,\
                [0] * DECIMAL_PLACES, other.decI,\
                False, other.negativeI)
        # d^2 = d/s3
        (s4ReIm, s4Deci, s4Neg) = longDivision(other.imag, s3ReIm,\
                other.decI, s3Deci,\
                other.negativeI, s3Neg)
        # c^2 + d^2 = s2 + s4 = x
        s2Num = Number(s2ReIm,0,s2Deci,[0] * DECIMAL_PLACES,s2Neg)
        s4Num = Number(s4ReIm,0,s4Deci,[0] * DECIMAL_PLACES,s4Neg)
        x = s2Num + s4Num
        # ac = a/(1/c) = a/s1
        (s5ReIm, s5Deci, s5Neg) = longDivision(self.real, s1ReIm,\
                self.decR, s1Deci,\
                self.negativeR, s1Neg)
        # bd = b/(1/d) = b/s3
        (s6ReIm, s6Deci, s6Neg) = longDivision(self.imag, s3ReIm,\
                self.decI, s3Deci,\
                self.negativeI, s3Neg)
        # ac + bd = s5 + s6 = f
        s5Num = Number(s5ReIm,0,s5Deci,[0] * DECIMAL_PLACES,s5Neg)
        s6Num = Number(s6ReIm,0,s6Deci,[0] * DECIMAL_PLACES,s6Neg)
        f = s5Num + s6Num
        # real = (ac+bd)/(c^2 + d^2) = f/x
        (real, decR, negativeR) = longDivision(f.real, x.real,\
                f.decR, x.decR, f.negativeR, x.negativeR)
        # bc = b/(1/c) = b/s1
        (s7ReIm, s7Deci, s7Neg) = longDivision(self.imag, s1ReIm,\
                self.decI, s1Deci, self.negativeI, s1Neg)
        # ad = a/(1/d) = a/s3
        (s8ReIm, s8Deci, s8Neg) = longDivision(self.real, s3ReIm,\
                self.decR, s3Deci, self.negativeR, s3Neg)
        # bc - ad =  s7 - s8 = g
        s7Num = Number(s7ReIm,0,s7Deci,[0] * DECIMAL_PLACES,s7Neg)
        s8Num = Number(s8ReIm,0,s8Deci,[0] * DECIMAL_PLACES,s8Neg)
        g = s7Num - s8Num
        # imag = (bc-ad)/(c^2 + d^2) = g/x
        (imag, decI, negativeI) = longDivision(g.real, x.real,\
                g.decR, x.decR, g.negativeR, x.negativeR)
        #print("END DIVISION\n")
        return Number(real, imag, decR, decI, negativeR, negativeI)
    
    # You can multiply numbers using the "*" operator
    def __mul__(self, other):
        """print("Multiply")
        print(self)
        print(other)"""
        n1 = Number(1)
        n2 = n1 / other
        n3 = self / n2
        #print("END MULTIPLICATION\n")
        return n3
    
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

# Add the real or imaginary parts of a Number
# xReIm: X left of decimal point, int
# yReIm: Y left of decimal point, int
# xDeci: X right of decimal point, list of ints
# yDeci: Y right of decimal point, list of ints
# negativeCondition: when to subtract carry
# Returns (zReIm, zDeci)
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

# Subtract the real or imaginary part of a number
# xReIm: X left of decimal point, int
# yReIm: Y left of decimal point, int
# xDeci: X right of decimal point, list of ints
# yDeci: Y right of decimal point, list of ints
# negativeCondition: when to subtract borrow
# negativeOutput: what sign changes if 0 and NC?
# Returns (zReIm, zDeci, negativeOutput)
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
        zReIm = xReIm + yReIm - borrow
    else:
        zReIm = xReIm + yReIm + borrow
    if (zReIm == 0 and negativeCondition):
        negativeOutput = True
    return (zReIm, zDeci, negativeOutput)

# Deprecated 12/24/2024
def multiply(xReIm, yReIm, xDeci, yDeci,\
             xIsNegative, yIsNegative):
    carry = 0
    zDeci = [0] * DECIMAL_PLACES
    zIsNegative = False
    for i in range(DECIMAL_PLACES - 1,-1,-1):
        t = carry + xDeci[i] + yDeci[i]
        if (t > 9):
            carry = int(str(t)[0])
            t = int(str(t)[1])
        else:
            carry = 0
        zDeci[i] = t
    if (xIsNegative != yIsNegative or
        (xIsNegative == True and yIsNegative == True)):
        zIsNegative = True
    zReIm = (xReIm + carry) * yReIm
    return (zReIm, zDeci, zIsNegative)

def longDivision(xReIm, yReIm, xDeci, yDeci,\
                 xIsNegative, yIsNegative):
    """print(xReIm)
    print(xDeci)
    print(yReIm)
    print(yDeci)
    print()"""
    if (yReIm == 0 and yDeci == [0] * DECIMAL_PLACES):
        #print("DIVIDE BY ZERO")
        """print(xReIm)
        print(xDeci)
        print(yReIm)
        print(yDeci)
        print()"""
        yDeci = ([0] * (DECIMAL_PLACES-1)) + [1]
        #return (99999999999999999999999999999,[9]*DECIMAL_PLACES,False)
        #return (0,[],False)
    # Obtain list of digits left of decimal
    # Ex. 480 -> [4,8,0]
    xLeft = list(str(xReIm))
    yLeft = list(str(yReIm))
    # Line up numbers
    if (len(xLeft) < len(yLeft)):
        xLeft = [0] * (len(yLeft) - len(xLeft)) + xLeft
    if (len(xLeft) > len(yLeft)):
        yLeft = [0] * (len(xLeft) - len(yLeft)) + yLeft
    # Full list of digits
    # Ex. 480.208 -> [4,8,0,2,0,8]
    digitsX = xLeft + xDeci
    digitsY = yLeft + yDeci
    
    # Result digits
    z = [None] * (len(xLeft) + DECIMAL_PLACES)
    
    # argX: 10984713424
    # argY:     2024323
    argX = ""
    argY = ""
    for j in range(len(digitsX)):
        argX += str(digitsX[j])
        argY += str(digitsY[j])
    argX = int(argX)
    argY = int(argY)
    
    
    m = 1
    nextZ = 0
    dif = 0
    if (argX >= argY):
        # m = 5426
        while (m*argY < argX):
            m += 1
        if (m*argY != argX):
            m -= 1
        
        # mArgY = 10983976598
        mArgY = m * argY
        # [None, None, '5','4','2','6',None...]
        strM = str(m)
        if (len(xLeft) > len(strM)):
            zerosFront = len(xLeft) - len(strM)
            for i in range(zerosFront):
                z[i] = "0"
            for i in range(len(strM)):
                z[i+zerosFront] = strM[i]
            nextZ = len(xLeft)
        else:
            # The multiple is too long!
            dif = len(strM) - len(xLeft)
            z = list(strM[:dif]) + z
            for i in range(dif,len(strM)):
                z[i] = strM[i]
            nextZ = len(xLeft) + dif
            
        argX = argX - mArgY
    else:
        for i in range(len(xLeft)):
            z[i] = "0"
        nextZ = len(z)-DECIMAL_PLACES

    #if (xReIm == 12):
    #    print(z)

    zeroFlag = False
    # Left to right
    while (nextZ < len(z)):
        if (argX < argY):
            argX *= 10
            if (zeroFlag):
                z[nextZ] = "0"
                nextZ += 1
            zeroFlag = True
            continue
        zeroFlag = False
        m = 1
        while (m*argY < argX):
            m += 1
        if (m*argY != argX):
            m -= 1
        z[nextZ] = str(m)
        nextZ += 1
        mArgY = m * argY
        argX = argX - mArgY
        if (nextZ == len(z)):
            #print("here")
            #print(z)
            #print(argX)
            #print(argY)
            if (argX < argY):
                if (argX*10 < argY):
                    continue
                else:
                    argX *= 10
            m = 1
            while (m*argY < argX):
                m += 1
            m -= 1
            if (m > 4):
                index = -1
                flag = True
                z[index] = str(int(z[index]) + 1)
                while z[index] == "10":
                    z[index] = "0"
                    z[index-1] = str(int(z[index-1]) + 1)
                    index -= 1
    
    
    zLeft = z[:len(xLeft) + dif]
    zReIm = ""
    for i in range(len(zLeft)):
        if (zLeft[i] != None): zReIm += zLeft[i]
    zReIm = int(zReIm)
    
    zDeci = z[len(xLeft) + dif:]
    for i in range(len(zDeci)):
        zDeci[i] = int(zDeci[i])
        
    if (xIsNegative == yIsNegative):
        zIsNegative = False
    else:
        zIsNegative = True
    
    return (zReIm, zDeci, zIsNegative)
    
# Determine which quantity (absolute value)
# is bigger.
# n1: X left of decimal, int
# d1: X right of decimal, list of ints
# n2: Y left of decimal, int
# d2: Y right of decimal, list of ints
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
"""
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
    
#def multiply(xReIm, yReIm, xDeci, yDeci,\
#             xIsNegative, yIsNegative):
#x = multiply(8,0,[0,0,6,0,8],[7,5,1,6,2],True, True)
#print(x)

# -109847.13424 + j8.00708
#     -20.24323 + j0.75162
x = Number(109,12,[9,9,9,9,9],[9,2,4,3,1])
y = Number(8,-999,[0,0,0,0,1],[0,0,0,0,0])
if (str(x / y) == "-0.01206 - j0.11020"):
    print("Test 21 Success!")
else:
    print("Test 21 Failed!")
    print(x/y)
print(x*y)
#longDivision(109847,20,[1,3,4,2,4],[2,4,3,2,3],False,False)
"""
