from RPLCD.i2c import CharLCD
import time

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

log0 = ""
log1 = ""
log2 = ""
log3 = ""

def lcdlog(x, y, words):
    log0 = words
    
def tempwrite(x, y, words):
    lcd.cursor_pos = (y,x)
    lcd.write_string(words)
    
    
def writewords(x, y, words):
    lcd.cursor_pos = (y,x)
    lcd.write_string(words)
    
def LCDoff():
    lcd.close(clear=True)

for b in range (xmax):
        entrance += '\x01'      
lcd.write_string(entrance)
lcd.write_string("\x01Welcome To\n\r\x01Maverick Bottling")
lcd.cursor_pos = (1,19)
lcd.write_string("\x01")
lcd.cursor_pos = (2,19)
lcd.write_string("\x01")
lcd.cursor_pos = (3,0)
lcd.write_string(entrance)
lcd.cursor_pos = (0,0)