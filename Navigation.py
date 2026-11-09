import Display as LCD
import Recipe_Storage as Rec
import time
import math
from decimal import Decimal

#10/31/2026
#Add save page navigation buttons
#Add parameter configuration button
#Global deligation only important if modifying the value. Not required for reading

#Command Code - Determines Action
overall_value=0
current_command=0
#999 - Landing Page
# 0 - Main Menu
# 1 - Dispense
# 2 - Recipe Select Page
# 3 - Settings Page
# 4 - Parameter Adjustment Page. Select Incrament to adjust by
# 5 - Parameter Adjustment Value Change
# 6 - Save Page

#Main Menu
main_value = 999
main_menu={}
#999 - Landing Page
# 0 - Dispense
# 1 - Recipe Select Page
# 2 - Recipe Select First
# 3 - Not a menu option - Settings page

#Recipe Parameters
#5 Recipes plus 1 extra for the done page. 0 Recipe is current recipe
Recipe_uppper_limit = 6
#3 Setting options plus 1 extra for the done/go back page
Settings_upper_limit = 3
#Main Menu Upper Limit
Main_upper_limit = 3

#Dynamically alter upper limit and lower limit based on recipe settings
# 1 Peristaltic Pump ml 000.00
#Upper limit 2
#Lower limit -3 (-2 + -1)
#2 Peristaltic Pump pulse per ml 0.00000
# Upper limit 0
# Lower limit -6 (-5 + -1)
#3 Diaphgram Pump ms 00000
#Upper limit 5
#Lower limmit -1 (0+-1)

#10^ amount of places limit + done. Example: xxxx.xx done
Increment_upper_limit = 0
Increment_lower_limit = 0

#Temporary value for parameter change
temp_value = 0

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

main_menu[Main_upper_limit] = {
	"Title": "Shutdown",
	#Safely Shutdown System
	"Command": 777
	}

#1/2 - Recipe Select Menu
#Recipe 0 - Current recipe
# Recipe 1 - 5 Recipe Selection
recipe_value = 0
recipe_menu={}

recipe_menu[0] = {
	"Title": "Current",
	"Command" : 0
	}

#3-Settings Select Menu
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

settings_menu[Settings_upper_limit] = {
	"Title": "Done",
	"Command" : 0
	}

#6 - Save Menu
save_value = 0
save_menu={}

settings_menu[0] = {
	"Title": "Save",
	"Command" : 3
	}

settings_menu[1] = {
	"Title": "Cancel",
	"Command" : 3
	}

#Select the 10^ value to modify or select done
increment_value = 0
#Modified value
parameter_value = 0

def navigation_select():
	#Declare modified global parameters

	global current_command
	global parameter_value
	global Increment_lower_limit
	global Increment_upper_limit
	
	match current_command:
		case 0:
			match main_value:
				case 0:
					current_command = 0
					return(Dispensing())
				#Recipe Selection For Loading
				case 1:
						current_command = 1
				#Recipe Selection Settings
				case 2:
						current_command = 2
				case Main_upper_limit:
					return(System_Shutdown())
				case 999:
					main_value=0
		#Load the value of the recipe to the main program
		case 1:
			if recipe_value == Recipe_uppper_limit:
				current_command = 0
			else:
				return(LoadingSetttings(recipe_value))
		#Select Recipe to be edited
		case 2:
			if recipe_value == Recipe_uppper_limit:
				current_command = 0
			else:
				current_command = 3
		#Load the recipe into a local system	
		case 3:
			if settings_value == Settings_upper_limit:
				current_command = 0
			else:
				if settings_value == 0:
					Increment_upper_limit = 2
					Increment_lower_limit = -3
				elif settings_value == 1:
					Increment_upper_limit = 0
					Increment_lower_limit = -6	
				elif settings_value == 2:
					Increment_upper_limit = 5
					Increment_lower_limit = -1
				parameter_value = Increment_upper_limit
				current_command = 4
		#Change parameter values up or down by incraments
		case 4:
			if Increment_lower_limit == increment_value:
				#Advance to save screen
				current_command = 6
			else:
				#Advance to change value
				current_command = 5
		#Change parameter values by decided incrament
		case 5:
			#Return to increment page to select new increment or to save
			current_command = 4
			#Reset increment adjusted by
			parameter_value = 0
		#Confirm Parameter Changes Save/Cancel
		case 6:
			#Save Recipe
			if save_value == 0:
				SaveRecipe()
			#Return to main menu
			command_value = 0
			
	if current_command == 0 or current_command == 3 or current_command == 6:
		scroll_disp(nav_menu, 0)
	elif current_command == 1 or current_command == 2:
		recipe_disp(0)
	elif current_command == 4:
		ValueDisplay()
		InitialZeros():
		ValueIncrement(0)
	elif current_command == 5:
		ValueChange(True, menu_number)
		print("current command error")
	
def navigation_up():
	#Declare modified global parameters
	global main_value
	global recipe_value
	global settings_value
	global current_command
	global increment_value
	global parameter_value
	global save_value
	
	match current_command:
		case 0:
			if main_value < Main_upper_limit:
				main_value+=1
			else:
				main_value = 0
			nav_menu = main_menu
			menu_number = main_value		
		case 1 | 2:
			if recipe_value < Recipe_uppper_limit:
				recipe_value+=1
			else:
				recipe_value = 0
			menu_number = recipe_value
		case 3:
			if settings_value < Settings_upper_limit:
				settings_value+=1
			else:
				settings_value = 0
			nav_menu = settings_menu
			menu_number = settings_value
		#Change parameter values up or down by incraments
		case 4:
			if increment_value < Increment_upper_limit:
				increment_value+=1
			else:
				increment_value = Increment_lower_limit
			menu_number = increment_value
		#Change parameter values by decided incrament
		case 5:
			parameter_value+=1
		menu_number = parameter_value
		#Confirm Parameter Changes Save/Cancel
		case 6:
			if save_value < 1:
				save_value -= 1
			else:
				save_value = 0
			menu_number = save_value

#Execute associated function			
	if current_command == 0 or current_command == 3 or current_command == 6:
		scroll_disp(nav_menu, menu_number)
	elif current_command == 1 or current_command == 2:
		recipe_disp(menu_number)
	elif current_command == 4:
		ValueIncrement(menu_number)
	elif current_command == 5:
		ValueChange(True, menu_number)
	else:
		print("current command error")

			
def navigation_down():
	#Declare modified global parameters
	global main_value
	global recipe_value
	global settings_value
	global current_command
	global increment_value
	global parameter_value
	global save_value
	
	match current_command:
		case 0:
			if main_value > 0:
				main_value -= 1
			elif main_value == 999:
				main_value = 0
			else:
				main_value = Main_upper_limit
			nav_menu = main_menu
			menu_number = main_value	
		case 1 | 2:
			if recipe_value > 0:
				recipe_value-=1
			else:
				recipe_value = Recipe_uppper_limit
			menu_number = recipe_value
		case 3:
			if settings_value > 0:
				settings_value-=1
			else:
				settings_value = Settings_upper_limit
			nav_menu = settings_menu
			menu_number = settings_value
		#Change parameter incraments
		case 4:
			if increment_value > Increment_lower_limit:
				increment_value-=1
			else:
				increment_value = Increment_upper_limit
			menu_number = increment_value
		#Change parameter values by decided incrament
		case 5:
			if parameter_value < 0:
				parameter_value = 9
			else:
				parameter_value -= 1
			menu_number = parameter_value
		#Confirm Parameter Changes Save/Cancel
		case 6:
			if save_value > 0:
				save_value -=1
			else:
				save_value = 1
			menu_number = save_value
	
	if current_command == 0 or current_command == 3 or current_command == 6:
		scroll_disp(nav_menu, menu_number)
	elif current_command == 1 or current_command == 2:
		recipe_disp(menu_number)
	elif current_command == 4:
		ValueIncrement(menu_number)
	elif current_command == 5:
		ValueChange(False, menu_number)
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
		#If iterator number is a recipe number
		#Upper Limit is the "back command"	
		if iterator != Recipe_uppper_limit:
			Recipe_Number=Rec.singleLoad(iterator)
		if iterator == 0:
			words1 = f"Current:{Recipe_Number.P_pump_ml}ml"
			words2 = f"{Recipe_Number.P_pump_tune}ml/p {Recipe_Number.D_pump_ms}ms"
		elif iterator == Recipe_uppper_limit:
			words1 = "Return To"
			wrods2 = "Main Menu"
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

#Return value to main program to know it is time to dispense	
def Dispensing():
	print("Dispensing")

def ValueDisplay():
	rnum = recipe_value
	snum = settings_value
	# Load the recipe and display neccessary information on to line
	Recipe_Number=Rec.singleLoad(rnum)
	#Peristalstic ml
	if snum == 0:
	words = f" Current:{Recipe_Number.P_pump_ml}ml"
	
	elif snum == 1:
	words = f" Current:{Recipe_Number.P_pump_tune}ml/p"
	
	elif snum == 2:
	words = f" Current:{Recipe_Number.D_pump_ms}ms"
		
	else:
		print ("snum out of range during iteration")
		
	LCD.writewords(0, 0, words, True)

#Incrament value will have a chevron that travels along the bottom based on what 10th power is being changed.
#Different settings will have different limits
def ValueIncrement(inum):
	mnnum = Increment_lower_limit
	mxnum = Increment_upper_limit
	total_increments = abs(mnnum)+abs(mxnum)
	total_spaces = inum * " "
	chevron = LCD.symb_chev
	#Compensate for decimal place
	if inum > mxnum:
		 total_spaces += " "
	# Add 3 chevrons for the word "Done"
	elif inum == total_increments:
		chevron = LCD.symb_chev * 4
	
	words = total_spaces + chevron
	
	LCD.writewordswithnav(0, 3, words, True)

	
def InitialZeros():
	zerosup = Increment_upper_limit
	zerosdown = abs(Increment_lower_limit) - 1
	words = zerosup * "0"
	if zerosdown > 0:
		words += "." + zerosdown * "0"
	words += "Done"
	LCD.writewordswithnav(0, 2, words, True)
	

#True Polarity Means Up
#False Polarity Means Down
#The value of change will be 10^incrament value.
#Within the display routine determine the length of the string, how many decimal places there are.
#When the value gets printed to screen keep specific format for number for ms it will be 00000. For tune it will be 0.00000. For persitalstic it will be 000.00
#10^ = parameter_value-increment_value
def ValueChange(polarity, pnum):
	global temp_value
	expo = Increment_upper_limit - increment_value
	# add value
	if polarity == True:
		temp_value += (10 ** expo) * pnum
	
	elif polarity == False:
		temp_value -= (10 ** expo) * pnum
	
	#define largest multiple
	upper_limit = 10 ** Increment_upper_limit
	lower_limit = 10 ** Increment_lower_limit
	remainder_only = temp_value % 1
	
	#Determine how many editable zeros there are
	if upper_limit >= temp_value:
		if temp_value != 0:
			big_zero_calc = temp_value
		#temp value == 0
		else:
			big_zero_calc = 1
			zeros_bigger = math.log10(upper_limit) - math.log10(big_zero_calc)
		words = math.floor(zeros_bigger) * "0"
		
	words += temp_value
	
	#Python float < 0 should convert to 0.x	
	# Add decimal place when needed	
	#if remainder_only == 0 and lower_limit < 0:
		#words += "."
	
	#All zeros pre-written should only need to determine how many zeros are in front.
	#proceeding logic is for other instances or if that is not true.	
	#if lower_limit < remainder_only:
		#smaller_decimal = Decimal(str(lower_limit))
		#larger_decimal = Decimal(str(remainder_only))
		#if smaller_decimal.as_tuple().exponent < 0:
			#compare1 = -smaller_decimal.as_tuple().exponent
		#else:
			#compare1 = 0
			
		#if larger_decimal.as_tuple().exponent < 0:
			#compare2 = -larger_decimal.as_tuple().exponent
		#else:
			#compare2 = 0
	
		#zeros_smaller = compare2 - compare1
		#words += zeros_smaller * "0"
	
	words += "Done"
	LCD.writewordswithnav(0, 2, words, False)
	
def SaveRecipe():
	print("Save New Parameter")

def System_Shutdown():
	print("Shutting Down")
	
try:
	initial_disp()
except:
	print("Failure at Navigation")
