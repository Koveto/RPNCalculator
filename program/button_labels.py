class ButtonLabels:
    ALTERNATE_FUNCTIONS = "Alternate Functions"
    SWAP = "Swap"
    ZERO = "0"
    DECIMAL_POINT = "Decimal Point"
    ADD = "Add"
    NATURAL_LOG = "Natural Log"
    COMPLEX_NUMBER = "Complex Number"
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
    
    ROW_7_A = (ANGLE,                ABS,     RECIPROCAL, ARCSINE,       ARCCOSINE,    ARCTANGENT)
    ROW_6_A = (SPLIT_COMPLEX_RECT,   SQRT,    SWAP,       SINE,          COSINE,       TANGENT)
    ROW_5_A = (ENTER,                ENTER,   BACKSPACE,  CLEAR,         SQUARE,       POWER)
    ROW_4_A = (SCIENTIFIC_NOTATION,  SEVEN,   EIGHT,      NINE,          DIVIDE,       POWER_OF_TEN)
    ROW_3_A = (CONJUGATE,            FOUR,    FIVE,       SIX,           MULTIPLY,     LOGARITHM)
    ROW_2_A = (COMPLEX_NUMBER,       ONE,     TWO,        THREE,         SUBTRACT,     EXPONENTIAL)
    ROW_1_A = (ALTERNATE_FUNCTIONS,  NEGATE,  ZERO,       DECIMAL_POINT, ADD,          NATURAL_LOG)

    BUTTON_LABELS_A = (ROW_1_A,\
                       ROW_2_A,\
                       ROW_3_A,\
                       ROW_4_A,\
                       ROW_5_A,\
                       ROW_6_A,\
                       ROW_7_A)
    
    ROW_7_B = (IMAG,                 REAL,    RECIPROCAL, ARCSINE,       ARCCOSINE,    ARCTANGENT)
    ROW_6_B = (SPLIT_COMPLEX_POLAR,  SQRT,    SWAP,       SINE,          COSINE,       TANGENT)
    ROW_5_B = (ENTER,                ENTER,   BACKSPACE,  CLEAR,         SQUARE,       POWER)
    ROW_4_B = (SCIENTIFIC_NOTATION,  SEVEN,   EIGHT,      NINE,          DIVIDE,       POWER_OF_TEN)
    ROW_3_B = (CONJUGATE,            FOUR,    FIVE,       SIX,           MULTIPLY,     LOGARITHM)
    ROW_2_B = (COMPLEX_NUMBER,       ONE,     TWO,        THREE,         SUBTRACT,     EXPONENTIAL)
    ROW_1_B = (ALTERNATE_FUNCTIONS,  NEGATE,  ZERO,       DECIMAL_POINT, ADD,          NATURAL_LOG)

    BUTTON_LABELS_B = (ROW_1_B,\
                       ROW_2_B,\
                       ROW_3_B,\
                       ROW_4_B,\
                       ROW_5_B,\
                       ROW_6_B,\
                       ROW_7_B)
