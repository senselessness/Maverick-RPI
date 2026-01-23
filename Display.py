from RPLCD.i2c import CharLCD
import time
import threading
#Avoid calling functions with lock() underneath a function that already is using with lock()
#Doing so will freeze the program

lock=threading.Lock()

xmax = 20
ymax = 4
space20="                    "
entrance = ""
for b in range (xmax):
    entrance += '\x01' 
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

#Establishes logs for stored data
class log:
    def __init__(self, message, xpos, ypos):
        self.message=message
        self.xpos=xpos
        self.ypos=ypos

#Creates list of logs
writtenlog = []
for a in range (ymax):
    writtenlog.append(log("\x00\x01\x00",0,a))

#Adds words written to log
def _lcdlog(x, y, words):
    if y < ymax:
        writtenlog[y].message = words
        writtenlog[y].xpos = x
    else:
        print("y value out of range")
        

#Temporarily writes words to a line. When the designated clock time is up,
#it frees itself and re-writes with the data logged for the line 
def _tempwrite(x, y, words, clock):
    _clearline(y)
    with lock:
        lcd.cursor_pos = (y,x)
        lcd.write_string(words)
    time.sleep(clock)
    _writeLogLine(y)
    
#Important words that will be logged on the line
#For this project, this is IP and port information that will be saved to the
def writewordslog(x, y, words):
    clearline(y)
    lcdlog(x,y,words)
    with lock:
        lcd.cursor_pos = (y,x)
        lcd.write_string(words)

def writewords(x, y, words):
    clearline(y)
    with lock:
        lcd.cursor_pos = (y,x)
        lcd.write_string(words)

#writes entire log instead of just a line
def writeLog():
    with lock:
        for a in range(len(writtenlog)):
            lcd.cursor_pos = (writtenlog[a].ypos,writtenlog[a].xpos)
            lcd.write_string(writtenlog[a].message)

#writes a single log line
def writeLogLine(y):
        _clearline(y)
        with lock:
            lcd.cursor_pos = (writtenlog[y].ypos,writtenlog[y].xpos)
            lcd.write_string(writtenlog[y].message)

#Write something to the LCD temporarily
def ThreadTemp(x, y, words, clock):
    tempwrite=threading.Thread(target=_tempwrite, args = (x,y,words,clock,))
    tempwrite.start()
    
#Write something to the LCD and Log it
def ThreadClearLine(y, clock):
    templineclear=threading.Thread(target=_ClearLineTemp, args = (y,clock,))
    templineclear.start()

#Temporarily Erase Line For Cleaner Messaging                
def _ClearLineTemp(y, clock):
    with lock:
        lcd.cursor_pos = (y,0)
        lcd.write_string(space20)
    time.sleep(clock)
    _writeLogLine(y)
    
#clears the line by writing spaces to it
def clearline(y):
    with lock:
        lcd.cursor_pos = (y,0)
        lcd.write_string(space20)

#clears LCD screen of any characters
def LCDoff():
    with lock:
        lcd.close(clear=True)

#Introduction/Start-Up Message
def _introduction():
    with lock:     
        lcd.write_string(entrance)
        lcd.write_string("\x01Welcome To\n\r\x01Mavrik Bottling")
        lcd.cursor_pos = (1,19)
        lcd.write_string("\x01")
        lcd.cursor_pos = (2,19)
        lcd.write_string("\x01")
        lcd.cursor_pos = (3,0)
        lcd.write_string(entrance)
        lcd.cursor_pos = (0,0)
        time.sleep(3)

_introduction()
ThreadLog(0,0,"\x01 Access settings")
ThreadLog(0,1,"\x01 Type in browser")
ThreadLog(0,2,"\x01 10.0.0.144:8000")
ThreadLog(0,3,"\x01 While on Wi-Fi")
time.sleep(8)
ThreadTemp(0,0,"Machine Started",2)
ThreadTemp(0,1,"\x01 I love my GF \x01",4)
ThreadTemp(0,2,"\x00 She is awesome \x00",4)
ClearLineTemp(3,4)
#Temp clear
time.sleep(7)
LCDoff()
