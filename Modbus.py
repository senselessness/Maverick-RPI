import minimalmodbus
import serial

import time

import Relay_Hat as Relay
#Relay wired into currently is 1

Relay.relayOn(1)
time.sleep(2)

class ModID:
    
    def __init__(
    self,
    address: int,
    mlperpulse: float,
    port='/dev/ttyUSB0',
    baudrate=9600,
    bytesize=8,
    stopbits=1,
    timeout=1,
    ):
        self.address=address
        self.device=minimalmodbus.Instrument(port,address)
        self.device.serial.baudrate=baudrate
        self.device.serial.bytesize=bytesize
        self.device.serial.stopbits=stopbits
        self.device.serial.timeout=timeout
        
        self.device.serial.parity=minimalmodbus.serial.PARITY_NONE
        
        self.device.mode=minimalmodbus.MODE_RTU
        
        self.device.close_port_after_each_call=True
        
        #Temporary
        self.device.debug=True
        

First_Pump=ModID(1,10.1)

def parameter_setup(ModID):
    #Current Stepper I have is most likely NEMA 17.
    #Configure to NEMA17 standards + whatever data I can gather on Lefoo LFP203ST.
    #Amp pull .<4A but effective current must be higher
    #Amp draw Pulses Per Rev
    AandPsetting=[2000, 200]
    #RPM, Accel, Decel, Max Speed
    SpeedSetting=[300, 100, 100, 500]

    registeraddress=int("1E",16)
    ModID.device.write_registers(registeraddress,AandPsetting)

    registeraddress=int("30",16)
    ModID.device.write_registers(registeraddress,SpeedSetting)



def motor_target(ModID, Target):
    
    #Pulse Target, Total Count
    TargetSetting=[Target, 0]
    registeraddress=int("34",16)
    ModID.device.write_registers(registeraddress,TargetSetting) 
    motor_run(ModID)
    
    
def motor_run(ModID):
    
    #Enable Motor
    registeraddress=int("39",16)
    #address in hex, value, number of decimals, funtion code
    #Function code of 6 means single address
    #Function code of 16 (default) means multiple. Specified if doing float.
    ModID.device.write_register(registeraddress,1,0,6)
    #Start Relative Position Mode
    registeraddress=int("37",16)
    ModID.device.write_register(registeraddress,2,0,6)

def mod_command(ModID,Hex_register):

    register_address=int(Hex_register,16)
try:
    parameter_setup(First_Pump)
    motor_target(First_Pump, 800)
    #print("Reading holding register at address 33")
    #data = First_Pump.device.read_register(33,number_of_decimals=0,functioncode=3)
    #print(f"This is it: {data}")
    
except Exception as e:
    print(e)

time.sleep(10)
Relay.relayOff(1)