from RPLCD.i2c import CharLCD
import time

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

#Create symbol for navigation
#Note made 09/28/2026
arrow_up = (
    0b00100,
    0b01110,
    0b11111,
    0b11111,
    0b00100,
    0b00100,
    0b00100,
    0b00000
    )

#Arrow Down Symbol
arrow_down = (
    0b00000,
    0b00100,
    0b00100,
    0b00100,
    0b11111,
    0b11111,
    0b01110,
    0b00100
    )

#Arrow Right Symbol
arrow_right = (
	0b10000,
    0b11000,
    0b11110,
    0b11111,
    0b11111,
    0b11110,
    0b11000,
    0b10000
    )
#Arrow Left Symbol
arrow_left = (
	0b00001,
    0b00011,
    0b01111,
    0b11111,
    0b11111,
    0b01111,
    0b00011,
    0b00001
    )   

lcd = CharLCD('PCF8574', 0x27)
lcd.create_char(0, smiley)
lcd.create_char(1, heart)
lcd.create_char(2, arrow_up)
lcd.create_char(3, arrow_down)
lcd.create_char(4, arrow_right)
lcd.create_char(5, arrow_left)


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
    clearline(y)
    lcd.cursor_pos = (y,x)
    lcd.write_string(words)
    time.sleep(clock)
    writeLogLine(y)
    
#Important words that will be logged on the line
def writewordslog(x, y, words):
    clearline(y)
    _lcdlog(x,y,words)
    lcd.cursor_pos = (y,x)
    lcd.write_string(words)

def writewords(x, y, words, clear):
	if clear:
		clearline(y)
	
	lcd.cursor_pos = (y,x)
	lcd.write_string(words)

#writes entire log instead of just a line
def writeLog():
	for a in range(len(writtenlog)):
		lcd.cursor_pos = (writtenlog[a].ypos,writtenlog[a].xpos)
		lcd.write_string(writtenlog[a].message)

#writes a single log line
def writeLogLine(y):
        clearline(y)
        lcd.cursor_pos = (writtenlog[y].ypos,writtenlog[y].xpos)
        lcd.write_string(writtenlog[y].message)

#clears the line by writing spaces to it
def clearline(y):
     lcd.cursor_pos = (y,0)
     lcd.write_string(space20)

#clears LCD screen of any characters
def LCDoff():
	lcd.close(clear=True)

#Stops Communication        
def LCDclose():
	lcd.close(clear=False)

#Introduction/Start-Up Message
def _introduction():   
        lcd.write_string(entrance)
        lcd.write_string("\x01Welcome To\n\r\x01Mavrik Bottling")
        lcd.cursor_pos = (1,19)
        lcd.write_string("\x01")
        lcd.cursor_pos = (2,19)
        lcd.write_string("\x01")
        lcd.cursor_pos = (3,0)
        lcd.write_string(entrance)
        lcd.cursor_pos = (0,0)
        time.sleep(5)
        lcd.close()

def navigationbar():
	lcd.cursor_pos = (0,0)
	lcd.write_string("\x04")
	lcd.cursor_pos = (1,0)
	lcd.write_string("\x02")
	lcd.cursor_pos = (3,0)
	lcd.write_string("\x03")
	lcd.cursor_pos = (0,0)
	lcd.close()

def valueline(valuename, value):
	lcd.cursor_pos = (1,0)
	lcd.write_string(f"{valuename}: {value}")
	
	
def valuechange(valuename, value):
	lcd.cursor_pos = (0,0)
	lcd.write_string("\x02")
	valueline(valuename, value)
	lcd.cursor_pos = (2,0)
	lcd.write_string("\x04")
	lcd.cursor_pos = (3,0)
	lcd.write_string("\x03")
	lcd.cursor_pos = (0,0)
	lcd.close()

try:
	_introduction()
	lcd.clear()
	navigationbar()
except:
	print("LCD Error")

if __name__=='__main__':
    LCDoff()
