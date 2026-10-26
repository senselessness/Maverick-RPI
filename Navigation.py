import Display as LCD
import Recipe_Storage as Rec
import time


#Command Code - Determines Action
overall_value=0
current_command=0
#999 - Landing Page
# 0 - Main Menu
# 1 - Dispense
# 2 - Recipe Select Page
# 3 - Settings Page

#Main Menu
main_value = 999
main_menu={}
#999 - Landing Page
# 0 - Main Menu
# 1 - Dispense
# 2 - Recipe Select Page
# 3 - Recipe Select First
# 4 - Not a menu option - Settings page


main_menu[999] = {
	"Title0": "Welcome Mavrik!",
	"Title1": "Press any button",
	"Title2": "to continue",
	#If associated with navigation. Command tells it what to do
	"Command": 0
	}

main_menu[0] = {
	"Title": "Dispense",
	#If associated with navigation. Command tells it what to do
	"Command": 1
	}
		
main_menu[1] = {
	"Title": "Recipe Select",
	#If associated with navigation. Command tells it what to do
	"Command": 2
	}

main_menu[2] = {
	"Title": "Settings",
	#Open Settings Navigation Menu
	"Command": 2
	}

#Recipe Select Menu
#Recipe 0 - Current recipe
# Recipe 1 - 5 Recipe Selection
recipe_value = 0
recipe_menu={}

recipe_menu[0] = {
	"Title": "Current",
	"Command" : 0
	}

#Settings Select Menu
#Select Recipe First
#0 - P_pump_ml
#1 - P_pump_tune
#2 - D_pump_ms

settings_value = 0
settings_menu={}

settings_menu[0] = {
	"Title": "Peristaltic ml",
	"Command" : 3
	}

settings_menu[1] = {
	"Title": "Peristaltic p/ml",
	"Command" : 3
	}

settings_menu[2] = {
	"Title": "Diaphragm ms",
	"Command" : 3
	}

settings_menu[3] = {
	"Title": "Done",
	"Command" : 0
	}
#Retrieve Command Number From Current Page

def navigation_select():
	match current_command:
		case 0:
			match main_value:
				case 0:
					current_comman = 0
					return(Dispensing())
				case 1 | 2:
					current_command = 2
				case 999:
					main_value=0
		#Load the value of the recipe to the main program
		case 1:
				return(LoadingSetttings(recipe_value))
		#Load the recipe into a local system
		case 2:
			return(ConfigureSettings(recipe_value,settings_value)
			
	scroll_disp(nav_menu, menu_number)
	
def navigation_up():
	#Declare modified global parameters
	global main_value
	global recipe_value
	global settings_value
	global current_command
	match current_command:
		case 0:
			if main_value < 2:
				main_value+=1
			else:
				main_value = 0
			nav_menu = main_menu
			menu_number = main_value		
		case 1 | 2:
			if recipe_value < 5:
				recipe_value+=1
			else:
				recipe_value = 0
			menu_number = recipe_value
		case 3:
			if settings_value < 3:
				settings_value+=1
			else:
				settings_value = 0
			nav_menu = settings_menu
			menu_number = settings_value
	if current_command == 0 or current_command == 3:
		scroll_disp(nav_menu, menu_number)
	elif current_command == 1 or current_command == 2:
		recipe_disp(menu_number)
	else:
		print("current command error")

			
def navigation_down():
	#Declare modified global parameters
	global main_value
	global recipe_value
	global settings_value
	global current_command
	match current_command:
		case 0:
			if main_value > 0:
				main_value -= 1
			elif main_value == 999:
				main_value = 0
			else:
				main_value = 2
			nav_menu = main_menu
			menu_number = main_value	
		case 1 | 2:
			if recipe_value > 0:
				recipe_value-=1
			else:
				recipe_value = 5
			menu_number = recipe_value
		case 3:
			if settings_value > 0:
				settings_value-=1
			else:
				settings_value = 3
			nav_menu = settings_menu
			menu_number = settings_value
	if current_command == 0 or current_command == 3:
		scroll_disp(nav_menu, menu_number)
	elif current_command == 1 or current_command == 2:
		recipe_disp(menu_number)
	else:
		print("current command error")

def initial_disp():	
	x=1
	for y in range(3):
		words = main_menu[999].get(f"Title{y}", f"Failed{y}")
		LCD.writewords(x, y, words, False)

def scroll_disp(menu, number):
	x=0
	index=0
	temp_list = []
	#Parse through nested dictionary
	for key, index_dict in menu.items():
		if key < 900:
			wl=index_dict.get("Title")
			temp_list.append(wl)
		#number-=1
	for words in temp_list[number:] + temp_list[:number]:
		if index < 4:
			LCD.writewordswithnav(x, index, words, True)
		index+=1
	
	
#Select for recipe load
#Select for settings edit
def recipe_disp(number):
	x = 0
	iterator=number
	for i in range(0,3,2):
		if iterator > 5:
			iterator = 0
		elif iterator < 0:
			iterator = 5
		Recipe_Number=Rec.singleLoad(iterator)
		if iterator == 0:
			words1 = f"Current:{Recipe_Number.P_pump_ml}ml"
			words2 = f"{Recipe_Number.P_pump_tune}ml/p {Recipe_Number.D_pump_ms}ms"
		else:
			words1 = f"#{Recipe_Number.SystemNumber}:{Recipe_Number.P_pump_ml}ml"
			words2 = f"{Recipe_Number.P_pump_tune}ml/p {Recipe_Number.D_pump_ms}ms"
		iterator = number+1
		LCD.writewordswithnav(x, i, words1, True)
		LCD.writewordswithnav(x, i+1, words2, True)

#In Collaboration With Main Menu Navigation 10/25/2026
def LoadingSetttings(Recipe_Number):
	print("Loaded Recipe")

#Add the opption to save/cancel	
def ConfigureSettings(Recipe_Number,Value):
	print("Configure Settings")
	
def Dispensing():
	print("Dispensing")

def ValueChange():
	print("Value Changed")
	
try:
	initial_disp()
	time.sleep(1)
	current_command=3
	time.sleep(1)
	navigation_down()
	time.sleep(1)
	navigation_up()
	time.sleep(1)
	navigation_up()
	time.sleep(1)
	navigation_up()
	time.sleep(1)
	navigation_up()
	time.sleep(1)
	navigation_up()
	time.sleep(1)
	navigation_up()
	time.sleep(1)
	navigation_down()
	time.sleep(1)
	navigation_down()
	time.sleep(1)
	navigation_down()
	time.sleep(1)
	navigation_down()
	time.sleep(1)
	navigation_down()
	time.sleep(1)
	navigation_down()
	time.sleep(1)
	navigation_down()
	time.sleep(1)
except:
	print("Failure at Navigation")
