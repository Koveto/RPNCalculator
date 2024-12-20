from machine import Pin
from gpio_lcd import GpioLcd
from time import sleep
import lcd, keypad
import button_constructor as bc

COLUMNS = 20
ROWS = 4

# Pinout assignment...
# LCD
RS = 16
E = 17
D4 = 18
D5 = 19
D6 = 20
D7 = 21
# Keypad
R1 = 0
R2 = 1
R3 = 2
R4 = 3
C1 = 4
C2 = 5
C3 = 6
# Buttons
BUTTON_PINS = [7,8,9,10,11,12,13,14,15,28,27,26]




#for button in buttons:
#    print(button)

def setup():
    # Set up I/O...
    # Set up LCD
    #lcd.newLCD(COLUMNS, ROWS, RS, E, D4, D5, D6, D7)
    lcdScreen = lcd.Lcd_Screen(COLUMNS, ROWS, RS, E, D4, D5, D6, D7)
    # Set up 4x3 Keypad
    keys = keypad.keypadInput(R1, R2, R3, R4, C1, C2, C3)
    # Set up buttons
    buttons = pushButtonList(BUTTON_PINS)


def main():
    
    setup()
    
    # Keep track of the last key
    lastKey = None
    
    # Display
    lcdScreen.cursor_at(11,2)
    lcdScreen.write("Y: 0.0000")
    lcdScreen.cursor_at(11,3)
    lcdScreen.write("X: 0.0000")
    
    while(True):
        
        # Scan buttons/keypad
        key = buttons.getKey()
        k = keys.getKey()
        if (k != None):
            key = k
        
        # A new key is pressed
        #if key != None and key != lastKey:
        #    interpretPress(key)
        #    display()
        #    lastKey = key
            
        # A key was released
        #elif key == None:
        #    lastKey = None
        
        sleep(0.1)
        
    
        

if __name__ == "__main__":
    main()