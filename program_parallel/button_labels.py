class ButtonLabels:
    ALTERNATE_FUNCTIONS = "Alternate Functions"
    SWAP = "Swap"
    ZERO = "0"
    DECIMAL_POINT = "Decimal Point"
    ADD = "Add"
    NATURAL_LOG = "Natural Log"
    COMPLEX_NUMBER = "Complex Number"
    COMPLEX_POLAR = "Complex Polar"
    ONE = "1"
    TWO = "2"
    THREE = "3"
    SUBTRACT = "Subtract"
    EXPONENTIAL = "Exponential"
    CONJUGATE = "Conjugate"
    FOUR = "4"
    FIVE = "5"
    SIX = "6"
    MULTIPLY = "Multiply"
    LOGARITHM = "Logarithm"
    SCIENTIFIC_NOTATION = "Scientific Notation"
    SEVEN = "7"
    EIGHT = "8"
    NINE = "9"
    DIVIDE = "Divide"
    POWER_OF_TEN = "Power of Ten"
    ENTER = "Enter"
    BACKSPACE = "Backspace"
    CLEAR = "Clear"
    SQUARE = "Square"
    POWER = "Power"
    SQRT = "Sqrt"
    NEGATE = "Negate"
    SINE = "Sine"
    COSINE = "Cosine"
    TANGENT = "Tangent"
    ANGLE = "Angle"
    ABS = "Abs"
    RECIPROCAL = "Reciprocal"
    ARCSINE = "Arcsine"
    ARCCOSINE = "Arccosine"
    ARCTANGENT = "Arctangent"
    IMAG = "Imag"
    REAL = "Real"
    SPLIT_COMPLEX_RECT = "SplitComplexRect"
    SPLIT_COMPLEX_POLAR = "SplitComplexPolar"
    PI = "Pi"
    SUM_PLUS = "SumPlus"
    SUM_MINUS = "SumMinus"
    E = "E"
    STO = "Store"
    RCL = "Recall"
    ROLL = "Roll"
    ORIENT = "Orientation"
    PERCENT = "Percent"
    DEG = "Degrees"
    RAD = "Radians"
    RADDEG = "Radians Degrees"
    RECPOL = "Rectangular Polar"
    
    ROW_7_A = (SUM_PLUS,             RECIPROCAL,      SQRT,          LOGARITHM,       NATURAL_LOG,    SPLIT_COMPLEX_RECT)
    ROW_6_A = (STO,                  RCL,             ROLL,          SINE,            COSINE,         TANGENT)
    ROW_5_A = (ENTER,                ENTER,           SWAP,          NEGATE,          E,              BACKSPACE)
    ROW_4_A = (ABS,                  SEVEN,           EIGHT,         NINE,            DIVIDE,         None)
    ROW_3_A = (ANGLE,                FOUR,            FIVE,          SIX,             MULTIPLY,       None)
    ROW_2_A = (ALTERNATE_FUNCTIONS,  ONE,             TWO,           THREE,           SUBTRACT,       None)
    ROW_1_A = (RADDEG,               ZERO,            DECIMAL_POINT, COMPLEX_POLAR,   ADD,            None)

    BUTTON_LABELS_A = (ROW_1_A,\
                       ROW_2_A,\
                       ROW_3_A,\
                       ROW_4_A,\
                       ROW_5_A,\
                       ROW_6_A,\
                       ROW_7_A)
    
    ROW_7_B = (SUM_MINUS,            POWER,           SQUARE,        POWER_OF_TEN,    EXPONENTIAL,               SPLIT_COMPLEX_POLAR)
    ROW_6_B = (COMPLEX_NUMBER,       PERCENT,         PI,            ARCSINE,         ARCCOSINE,                 ARCTANGENT)
    ROW_5_B = (ENTER,                ENTER,           SWAP,          NEGATE,          SCIENTIFIC_NOTATION,       CLEAR)
    ROW_4_B = (REAL,                 SEVEN,           EIGHT,         NINE,            DIVIDE,                    None)
    ROW_3_B = (IMAG,                 FOUR,            FIVE,          SIX,             MULTIPLY,                  None)
    ROW_2_B = (ALTERNATE_FUNCTIONS,  ONE,             TWO,           THREE,           SUBTRACT,                  None)
    ROW_1_B = (RECPOL,               DEG,             RAD,           CONJUGATE,       ORIENT,                    None)

    BUTTON_LABELS_B = (ROW_1_B,\
                       ROW_2_B,\
                       ROW_3_B,\
                       ROW_4_B,\
                       ROW_5_B,\
                       ROW_6_B,\
                       ROW_7_B)


