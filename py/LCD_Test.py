import LCD
import time
from machine import Pin
import random

Buzzer = Pin(13, Pin.OUT)
B0 = Pin(15,Pin.IN,Pin.PULL_UP)
B1 = Pin(14,Pin.IN,Pin.PULL_UP)

def Beep():
    Buzzer.value(1)
    time.sleep(0.02)
    Buzzer.value(0)
    
LCD.Init()

Foreground = LCD.RGB(250,200,0)
Background = LCD.RGB(0,0,50)
White = LCD.RGB(250,250,250)
Pink = LCD.RGB(250,150,150)
Yellow = LCD.RGB(250,250,0)
Cyan = LCD.RGB(0,250,250)
Magenta = LCD.RGB(250,0,250)
Red = LCD.RGB(250,0,0)

X0 = time.ticks_us()
LCD.Clear(Background)
X1 = time.ticks_us()
print('Clear: ',X1-X0,'us')

X0 = time.ticks_us()
LCD.Solid_Box(30,30,80,80,Yellow)
X1 = time.ticks_us()
print('Solid Box: ',X1-X0,'us')

X0 = time.ticks_us()
LCD.Box(20,20,470,310,Yellow)
X1 = time.ticks_us()
print('Box: ',X1-X0,'us')

X0 = time.ticks_us()
LCD.Circle(380,220,70,Yellow)
X1 = time.ticks_us()
print('Circle: ',X1-X0,'us')


X0 = time.ticks_us()
LCD.Lander(200,55,Yellow)
X1 = time.ticks_us()
print('LCD Lander: ',X1-X0,'us')


for i in range(1,7):
    X0 = time.ticks_us()
    LCD.Dice(i, 50, 250, Red, White)
    X1 = time.ticks_us()
print('Dice: ',X1-X0,'us')

for i in range(1,14):
    X0 = time.ticks_us()
    LCD.Card(i, 1, 150, 230)
    X1 = time.ticks_us()
print('Card: ',X1-X0,'us')


X0 = time.ticks_us()
LCD.Line(12, 12, 12, 315, Pink)
X1 = time.ticks_us()
print('LineY: ',X1-X0,'us')


X0 = time.ticks_us()
LCD.Line(400,20,470,315,Pink)
X1 = time.ticks_us()
print('Line: ',X1-X0,'us')


X0 = time.ticks_us()
LCD.Text2('Hello World',100,30,White, Background)
X1 = time.ticks_us()
print('Text2: ',X1-X0,'us')

X0 = time.ticks_us()
LCD.Text('Hello World', 100, 70, White, Background)
X1 = time.ticks_us()
print('Text 1: ',X1-X0,'us')

X0 = time.ticks_us()
Y = LCD.Shuffle()
X1 = time.ticks_us()
print('Shuffle: ',X1-X0,'us')


for i in range(1,10):
    x = i ** 0.4
    X0 = time.ticks_us()
    LCD.Number2(x, 10, 4, 50, 150, White, Background)
    X1 = time.ticks_us()
print('Number2 = ',X1-X0,'us')

for i in range(1,10):
    x = i ** 0.4
    X0 = time.ticks_us()
    LCD.Number(x, 10, 4, 50, 200, White, Background)
    X1 = time.ticks_us()
print('Number = ',X1-X0,'us')


for i in range(0,16):
    LCD.Number((16-i)%10, 1, 0, 100+15*i, 120, LCD.RGB(150,150,150),Background)
    
Ball = 1
while (True):
    while(B0.value() and B1.value()):
        pass
    if(B1.value() == 1):
        X = random.randrange(1,16)
        print('Fair Wheel',(X+Ball+48)%16+1)
    else:
        X = (16+6-Ball)
        print('Rigged Wheel',(X+Ball+48)%16+1)
    for i in range(0,X+48):
        Ball = (Ball + 1)%16
        LCD.Bar_Out(Ball+1, 100, 100)
        Beep()
        if(i < X+47):
            time.sleep(1 / (X+48-i))
    LCD.Number2(Ball+1, 2, 0, 370, 150, Foreground, Background)


