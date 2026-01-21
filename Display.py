from RPLCD.i2c import CharLCD
import time
import threading
#Avoid calling functions with lock() underneath a function that already is using with lock()
#Doing so will freeze the program

lock=threading.Lock()

xmax = 20
ymax = 4
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
def lcdlog(x, y, words):
    if y < ymax:
        writtenlog[y].message = words
        writtenlog[y].xpos = x
    else:
        print("y value out of range")
        

#Temporarily writes words to a line. When the designated clock time is up,
#it frees itself and re-writes with the data logged for the line 
def tempwrite(x, y, words, clock):
    clearline(y)
    with lock:
        lcd.cursor_pos = (y,x)
        lcd.write_string(words)
    time.sleep(clock)
    writeLogLine(y)
    
#Important words that will be logged on the line
#For this project, this is IP and port information that will be saved to the
def writewords(x, y, words):
    lcdlog(x,y,words)
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
        clearline(y)
        with lock:
            lcd.cursor_pos = (writtenlog[y].ypos,writtenlog[y].xpos)
            lcd.write_string(writtenlog[y].message)

#clears the line by writing spaces to it
def clearline(y):
    with lock:
        space20="                    "
        lcd.cursor_pos = (y,0)
        lcd.write_string(space20)

#clears LCD screen of any characters
def LCDoff():
    with lock:
        lcd.close(clear=True)

#Introduction/Start-Up Message
def introduction():
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


tempwrite0=threading.Thread(target=introduction)
tempwrite1=threading.Thread(target=tempwrite, args = (0,0,"I Love My GF",5,))
tempwrite2=threading.Thread(target=tempwrite, args = (0,1,"I Love My GF",7,))
#Starts then waits for introduction to be completed before stating other threads.
tempwrite0.start()
tempwrite0.join()
#Temp test lines
tempwrite1.start()
tempwrite2.start()



#Temp clear
time.sleep(10)
LCDoff()
