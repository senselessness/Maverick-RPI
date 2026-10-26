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
    
symb_smile="\x00"
symb_heart="\x01"
symb_up="\x02"
symb_down="\x03"
symb_right="\x04"
symb_left = "\x05"

lcd = CharLCD('PCF8574', 0x27)
lcd.create_char(0, smiley)
lcd.create_char(1, heart)
lcd.create_char(2, arrow_up)
lcd.create_char(3, arrow_down)
lcd.create_char(4, arrow_right)
lcd.create_char(5, arrow_left)


def writewords(x, y, words, clear):
	if clear:
		clearline(y)
	
	lcd.cursor_pos = (y,x)
	lcd.write_string(words)

def writewordswithnav(x, y, words, clear):
	if clear:
		clearline(y)
	#Add Navigation Bar to String
	if y == 0:
		words = symb_right + words
	elif y==1:
		words = symb_up + words
	elif y==2:
		words = " " + words
	elif y==3:
		words = symb_down + words
	else:
		print("LCD y error")
	
	lcd.cursor_pos = (y,x)
	lcd.write_string(words)
	LCDsleep()

#clears the line by writing spaces to it
def clearline(y):
     lcd.cursor_pos = (y,0)
     lcd.write_string(space20)
     LCDsleep()

#clears LCD screen of any characters
def LCDoff():
	lcd.close(clear=True)

#Stops Communication        
def LCDclose():
	lcd.close(clear=False)

#Required sleep intervval for multiple writes
def LCDsleep():
	time.sleep(.1)

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
       

def navigationbar():
	lcd.cursor_pos = (0,0)
	lcd.write_string("\x04")
	lcd.cursor_pos = (1,0)
	lcd.write_string("\x02")
	lcd.cursor_pos = (3,0)
	lcd.write_string("\x03")
	lcd.cursor_pos = (0,0)
	LCDsleep()
	

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
    
