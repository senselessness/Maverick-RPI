import minimalmodbus
import serial

class Mod_ID:
    
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
        self.mlperpulse=mlperpulse
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
        

#First_Pump=Mod_ID(1, 0.00375)

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



def motor_target_pulse(ModID, Target):
    
    #Pulse Target, Total Count
    TargetSetting=[Target, 0]
    registeraddress=int("34",16)
    ModID.device.write_registers(registeraddress,TargetSetting) 
    motor_run(ModID)

def motor_target_ml(ModID, Target):
    
    #Pulse Target, Total Count
    Target_ml=Target/ModID.mlperpulse
    TargetSetting=[round(Target_ml), 0]
    registeraddress=int("34",16)
    ModID.device.write_registers(registeraddress,TargetSetting) 
    motor_run(ModID)
    
    
def motor_run(ModID):
    
    #Enable Motor
    registeraddress=int("39",16)
    ModID.device.write_register(registeraddress,1,0,6)
    #Start Relative Position Mode
    registeraddress=int("37",16)
    ModID.device.write_register(registeraddress,2,0,6)
    
def motor_calibrate(ModID):
    motor_target(First_Pump, 8000)
    #user_yn=input("Was liquid dispensed the entire time? \n y/n:")
    #if user_yn=="y":
    #    ml_total=float(input("How many ml:"))
    #    First_Pump.mlperpulse = ml_total/8000
    #    print("Milliliter per pulse", First_Pump.mlperpulse, "ml")
    #else:
    #    user_yn=input("Try again? \n y/n:")
    #    if user_yn=="y":
    #        motor_calibrate(ModID)
    #    else:
    #        return

def mod_command(ModID,Hex_register):

    register_address=int(Hex_register,16)
try:
    parameter_setup(First_Pump)
    motor_target_ml(First_Pump, 21)
    #motor_calibrate(First_Pump)

except Exception as e:
    print(e)