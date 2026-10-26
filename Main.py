import time
from gpiozero import Button, LED, DigitalInputDevice, DigitalOutputDevice
import Relay_Hat as RH
import Modbus_Pump as Mod_P
import Navigation as Nav


int: menu_selected = 0
int: recipe_selected = 0

#BCM Pin Map To Current Input Pins
Select_button = Button(17)
Up_arrow = Button(27)
Dn_arrow = Button(22)

#Relay Addresses
P_pump=1
D_pump=4

#ACV Dispense Control
#Add event must be within the function loop for the callback to work
def acvFlow():
        RH.relayOn(ACVgateAddress)
        RH.relayOn(ACVpumpAddress)

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
    #Added LCDclose - Maybe causing pws issues by having serial communication open
    LCD.LCDclose()


getanddisplayconnect()

ACVstart.when_pressed = lambda x: Start_button(ACVDistribution)
ACVflow.when_activated = lambda x: Counter_Up(ACVDistribution)
ACVstop.when_pressed = lambda x: Stop_button(ACVDistribution)
