from machine import Pin
from gpio_lcd import GpioLcd
from time import sleep
import lcd

COLUMNS = 20
ROWS = 4

# Pinout assignment...
# LCD
RS = 28
E = 27
D4 = 26
D5 = 22
D6 = 21
D7 = 20

def main():
    
    lcdScreen = lcd.Lcd(COLUMNS, ROWS, RS, E, D4, D5, D6, D7)
    print(lcdScreen)
    
    lcdScreen.move_cursor(15,0)
    
    # Display
    lcdScreen.write("Y: 0.0000")
    lcdScreen.write("X: 0.0000")
    
    while(True):
        pass
        
    
        

if __name__ == "__main__":
    main()
