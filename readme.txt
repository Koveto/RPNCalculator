Reverse Polish Notation (RPN) Calculator

Contributors:
Kale Erickson
Kobe Goodwin
Gabe Wichmann

NDSU Senior Design project
ECE 403/405
Fall 2024 - Spring 2025
OneNote: https://ndusbpos-my.sharepoint.com/:o:/g/personal/kale_erickson_ndus_edu/EvFGwJnf-eBBiN7WtRWUvscBkYgOqBa3zW2gMm88qsdTBQ?e=oOiAU5

Project Description

HP-42S is a reverse polish notation (RPN) calculator championed by 
engineers around the world. RPN calculators sell for $400 and higher:
a forbidding price for college students. Our committee will design an
alternative HP-42S calculator that is affordable and reliable. Our 
RPN calculator solution will operate on mobile hardware powered by a
battery and disconnected from external devices. Our committee aims to
construct a RPN calculator engineering students could feasibly use on
exams. 

Instructions

1. Hold the button on the Raspberry Pi Pico
2. Plug the Pico into the computer
3. Drag "rp2-pico-micropython-doubleprecision-1-19.uf2" into the new directory
4. Unplug the Pico
5. Release the button
6. Plug the Pico into the computer
7. Use Thonny to save files in "program" to Pico

About the LCD

The program includes lcd.py and lcd_i2c.py.
lcd.py:
   communicates to the 20x4 LCD (using parallel interface)
lcd_i2c.py:
   NOT NECESSARY TO DOWNLOAD.
   used by an old PCB revision to communicate to its 16x2 LCD
   (using I2C protocol). 
To switch from one to the other,
   remove commented-out LCD_I2C import/initialization in main.py.
   comment out LCD import/initialization in main.py. 
Different LCD?
   the program only supports 20x4 parallel or 16x2 I2C.
   change ROWS and COLUMNS in lcd.py or lcd_i2c.py.
   revise lcd.write_to(...) commands in main.py and calculator.py.

Program your own game!

lcd.py is necessary.
Revise button_labels.py with your buttons and mapping.
Revise push_buttons.py if necessary.
Create your own main.py to read input and display output.