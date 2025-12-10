import time
import json
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
#BCM Pin Map To Current Output Pins
ACVgate = 23
ACVpump = 24

#BCM Pin Map To Current Input Pins
ACVstart = 17
ACVflow = 27
ACVstop = 22


JsonFile="Data.json"


#Used Global Data and Functions
class SystemVariables:
    SystemNumber = 0
    StopProcess = False
    StartProcess = False
    Counter = 0
    Target = 6
    Total_Product = 0
    SystemName = ""
    
    #Initialize
    def __init__(self,SystemNumber, SystemName):
        self.SystemNumber=SystemNumber
        self.SystemName=SystemName
        
ACVDistribution = SystemVariables(0, "Apple Cider Vinegar")
OilDistribution = SystemVariables(1, "Essential Oil")

#Edit Controls/Write To Memory
def writeControls():
    MachineDictionary = [
        {"identifier": ACVDistribution.SystemNumber,"name": "Apple Cider Vinegar Distribution", "target": ACVDistribution.Target, "total": ACVDistribution.Total_Product},
        {"identifier": OilDistribution.SystemNumber,"name": "Esstentail Oil Distribution", "target": OilDistribution.Target, "total": OilDistribution.Total_Product}
        ]
    
    Machinejson = json.dumps(MachineDictionary, indent=4)
    with open(JsonFile, "w") as json_file:
        json_file.write(Machinejson)
    print('Saved!')
    return();

#Read text template for any configured settings
def loadControls():
    with open(JsonFile,"r") as json_file:
        MachineDictionary = json.load(json_file)
    Loaded_Target=[x["target"] for x in MachineDictionary]
    Loaded_Total=[y["total"] for y in MachineDictionary]
    ACVDistribution.Target=Loaded_Target[0]
    ACVDistribution.Total_Product=Loaded_Total[0]
    OilDistribution.Target=Loaded_Target[1]
    OilDistribution.Total_Product=Loaded_Total[1]
    print ('Loaded!');


try:
    loadControls()
except:
    print('Initial Load\nNo System Information Saved')

#ACV Dispense Control
#Add event must be within the function loop for the callback to work
def acvFlow():
        GPIO.output(ACVgate, GPIO.HIGH)
        GPIO.output(ACVpump, GPIO.HIGH)

#oilMix Control
def oilMix():
    print('Oil Control Does Nothing At The Moment');
    
#Start Process - Boolean comes in through HTML link to start process.
#Try statements will ensure the program works. Joining before initiating will cause a runtime fault
def Start_button(Variables):
    if Variables.StartProcess == False:
        Variables.StartProcess=True
        if Variables.SystemNumber==0:
            print ('ACV transfer started')
            acvFlow()
        elif Variables.SystemNumber==1:
            print ('Oil Mix started')
            oilMix()
        
#Counter
def Counter_Up(Variables):
    if Variables.StartProcess==True:
        Variables.Counter+=1
        print('Counter Value = ', Variables.Counter)
        if Variables.Counter>=Variables.Target:
            Variables.StopProcess=True
            Variables.StartProcess=False
            Variables.Total_Product+=1
            print('Product Completed = ', Variables.Total_Product)
            Stop_button(Variables)

#Stop Process
#Stopping the process like this will remove all mapping. Find a better place for cleanup. In a shutdown routine or something
def Stop_button(Variables):
        if Variables.StartProcess==True or Variables.StopProcess==True:
            if Variables.SystemNumber==0:
                StopACV()
            elif Variables.SystemNumber==1:
                StopOil()
            Variables.StartProcess=False
            Variables.StopProcess=False
            Variables.Counter=0
            print ('Equipment Stopped')
        
def StopACV():
    GPIO.output(ACVpump,GPIO.LOW)
    GPIO.output(ACVgate, GPIO.LOW)
    
def StopOil():
    print('Oil Does Nothing At The Moment')

   
#Map Outputs
GPIO.setup(ACVgate, GPIO.OUT)
GPIO.setup(ACVpump, GPIO.OUT)

#Map Inputs
GPIO.setup(ACVstart, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(ACVflow, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(ACVstop, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

GPIO.add_event_detect(ACVstart,GPIO.FALLING, callback=lambda x: Start_button(ACVDistribution), bouncetime=300)
GPIO.add_event_detect(ACVflow,GPIO.FALLING, callback=lambda x: Counter_Up(ACVDistribution), bouncetime=1)
GPIO.add_event_detect(ACVstop,GPIO.FALLING, callback=lambda x: Stop_button(ACVDistribution), bouncetime=300)
