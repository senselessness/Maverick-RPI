from smbus import SMBus
import time

#Declare what I2C device you are working with
relay_hat = SMBus(1)
relay_address = 0x10
on = 0xFF
off = 0x00

def relayOn(relay_number):
    relay_hat.write_byte_data(relay_address, relay_number, on)
    
def relayOff(relay_number):
    relay_hat.write_byte_data(relay_address, relay_number, off)

def relayAllon():
    for a in range(1,5):
        relay_hat.write_byte_data(relay_address, a, on)

def relayAlloff():
    for a in range(1,5):
        relay_hat.write_byte_data(relay_address, a, off)

if __name__=='__main__':
    relayAlloff()