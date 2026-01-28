import time
import json
import netifaces
from gpiozero import Button, LED, DigitalInputDevice, DigitalOutputDevice
import Display as LCD
import Relay_Hat as RH

#BCM Pin Map To Current Output Pins
ACVgate = LED(23)
ACVpump = LED(24)

#BCM Pin Map To Current Input Pins
ACVstart = Button(17)
ACVflow = DigitalInputDevice(27)
ACVstop = Button(22)

#Relay Addresses
ACVgateAddress=1
ACVpumpAddress=2

#Log Variables
assigned_port=8080
Access_Info=""

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
        RH.relayOn(ACVgateAddress)
        RH.relayOn(ACVpumpAddress)
        ACVpump.on()
        ACVgate.on()

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
            LCD.writewords(0,0,"\x01 ACV Transfer")
            LCD.writewords(0,1,"\x01 Started")
            LCD.writewords(0,2, "\x01 Target: " + str(Variables.Target))
            LCD.clearline(3)
            acvFlow()
        elif Variables.SystemNumber==1:
            print ('Oil Mix started')
            oilMix()
        
#Counter
def Counter_Up(Variables):
    if Variables.StartProcess==True:
        Variables.Counter+=1
        LCD.writewords(0,3, "\x01 Count: " + str(Variables.Counter))
        print('Counter Value = ', Variables.Counter)
        if Variables.Counter>=Variables.Target:
            Variables.StopProcess=True
            Variables.StartProcess=False
            Variables.Total_Product+=1
            print('Product Completed = ', Variables.Total_Product)
            LCD.writewords(0,3,"\x01 Completed: " + str(Variables.Total_Product))
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
            LCD.writewords(0,0,"\x01 Equipment")
            LCD.writewords(0,1,"\x01 Stopped")
            LCD.ThreadClearLine(2,3)
            LCD.ThreadWriteLogWithDelay(3)
        
def StopACV():
        RH.relayOff(ACVgateAddress)
        RH.relayOff(ACVpumpAddress)
        ACVpump.off()
        ACVgate.off()
    
def StopOil():
    print('Oil Does Nothing At The Moment')
    
def peripherialsoff():
    LCD.LCDoff()
    RH.relayAlloff()

def getanddisplayconnect():
    try:
        address = netifaces.ifaddresses('wlan0')
        ip_address = address[netifaces.AF_INET][0]['addr']
        Access_Info= str(ip_address)+":"+str(assigned_port)
        print (ip_address)
        LCD.writewordslog(0,0,"\x01 Access settings")
        LCD.writewordslog(0,1,"\x01 Type in browser")
        LCD.writewordslog(0,2,"\x01 "+ Access_Info)
        LCD.writewordslog(0,3,"\x01 While on Wi-Fi")
    except:
        print("Error Retrieving IP address")
        LCD.writewordslog(0,0,"\x01 Device Not")
        LCD.writewordslog(0,1,"\x01 Able To")
        LCD.writewordslog(0,2,"\x01 Access")
        LCD.writewordslog(0,3,"\x01 Wi-Fi")


getanddisplayconnect()

ACVstart.when_pressed = lambda x: Start_button(ACVDistribution)
ACVflow.when_activated = lambda x: Counter_Up(ACVDistribution)
ACVstop.when_pressed = lambda x: Stop_button(ACVDistribution)