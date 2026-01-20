from RPLCD.i2c import CharLCD
import time
import asyncio

xmax = 20
ymax = 4
entrance = ""
#xpos 0 - 19
#ypos 0 - 3

smiley = (
    0b00000,
    0b01010,
    0b01010,
    0b00000,
    0b10001,
    0b01010,
    0b01110,
    0b00000
    )

heart = (
    0b00000,
    0b01010,
    0b11111,
    0b11111,
    0b11111,
    0b01110,
    0b00100,
    0b00000
    )

lcd = CharLCD('PCF8574', 0x27)
lcd.create_char(0, smiley)
lcd.create_char(1, heart)

class log:
    def __init__(self, message, xpos, ypos):
        self.message=message
        self.xpos=xpos
        self.ypos=ypos
    
writtenlog = []
for a in range (ymax):
    writtenlog.append(log("",0,a))

def lcdlog(x, y, words):
    if y < ymax:
        writtenlog[y].message = words
        writtenlog[y].xpos = x
    else:
        print("y value out of range")
        

#non-blocking task    
async def tempwrite(x, y, words, time):
    clearline(y)
    lcd.cursor_pos = (y,x)
    lcd.write_string(words)
    await asyncio.sleep(time)
    writeLog()
    
    
    
async def writewords(x, y, words, temp, time):
    if temp == True:
        temp_operation = asyncio.create_task(tempwrite(x,y,words,time))
    elif temp == False:
        lcdlog(x,y,words)
        lcd.cursor_pos = (y,x)
        lcd.write_string(words)
    else:
        print("Invalid Temp Parameter Parameter")
    
    #just a test
    print("doing other stuff...")
    await temp_operation 
    
def writeLog():
    for a in range(len(writtenlog)):
        lcd.cursor_pos = (writtenlog[a].ypos,writtenlog[a].xpos)
        lcd.write_string(writtenlog[a].message)

def clearline(y):
    #random stuff
    space20="                    "
    lcd.cursor_pos = (y,0)
    lcd.write_string(space20)
        
def LCDoff():
    lcd.close(clear=True)

for b in range (xmax):
        entrance += '\x01'      
lcd.write_string(entrance)
lcd.write_string("\x01Welcome To\n\r\x01Mavrik Bottling")
lcd.cursor_pos = (1,19)
lcd.write_string("\x01")
lcd.cursor_pos = (2,19)
lcd.write_string("\x01")
lcd.cursor_pos = (3,0)
lcd.write_string(entrance)
lcd.cursor_pos = (0,0)

asyncio.run(writewords(0,0, "I love my gf", True, 5))

#work on temp
#lcd.clear()
#awaits for asyncio.run to finish. Need to work around
LCDoff()