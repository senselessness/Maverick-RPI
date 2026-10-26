import json

JsonFile="Recipes.json"

class Recipe:	
	#Initialize
	def __init__(
	self,
	#Recipe identification number
	#Where it appears in sequence
	SystemNumber: int,
	P_pump_ml = 0.0,
	#Tune = ml/pulse
	#May need to be recalibrated based on enviroment or solution
	P_pump_tune = 0,
	D_pump_ms = 0,
	Total_Product = 0,
	):
		self.SystemNumber=SystemNumber
		self.P_pump_ml = P_pump_ml
		self.P_pump_tune=P_pump_tune
		self.D_pump_ms=D_pump_ms
		self.Total_Product=Total_Product
		
	def __repr__(self):
		message = ( 
		f"Recipe\n"
		f"System Number='{self.SystemNumber}'\n"
		f"Pump Target in ml = '{self.P_pump_ml}'\n" 
		f"Pump Tune Variable = '{self.P_pump_tune}'\n"
		f"Diaphragm Pump runtime in ms = '{self.D_pump_ms}'\n" 
		f"Product Produced = '{self.Total_Product}'\n" 
		)
		return message;
 
#Recipe 0 is the running recipe. The "loaded recipe"
#Present to be used in unique command events
recipe_list=[]

#Edit Controls/Write To Memory
def writeControls():
	with open(JsonFile, "w") as json_file:
		json.dump(recipe_list, json_file, default=lambda obj: obj.__dict__, indent=4)
	print('Saved!')
	return();

#Read text template for any configured settings
#Must load entire dictionary before parsing
#Dictionary comes in as list. May not need conversion back to list
def loadControls():
	with open(JsonFile,"r") as json_file:
		recipe_dictionary = json.load(json_file)
		#Convert all .json dictionaries back into an object
		recipe_list = [Recipe(**system_number) for system_number in recipe_dictionary]
		
		#Examples of how to retrieve information from dictionaries
		#Prints all values of the dict position
		#print (recipe_dictionary[0].values())
		#Prints all keys of the dict postion
		#print (recipe_dictionary[0].keys())
		#Prints the SystemNumber of the dict position
		#print (recipe_dictionary[0]["SystemNumber"])

		#Print specified position of .json as dict
		#print(recipe_dictionary[0])
		
		#Print the object object after converting all dicitonaries to an object
		#print(recipe_list[0])
		
	return recipe_list	
	print('Loaded all data to persistent list')
    
#Return Data Requested as Class
def singleLoad(Recipe_Number):
	try:
		with open(JsonFile,"r") as json_file:
			recipe_dictionary = json.load(json_file)
			isolated_recipe = Recipe(**recipe_dictionary[Recipe_Number])
		return isolated_recipe
	except:
		print(f"Recipe: {Recipe_Number} does not exist") 
		
#writes new modified recipe to database	
def singleWrite(Recipe_Number, key, value):
	try:
		with open(JsonFile,"r") as json_file:
			recipe_dictionary = json.load(json_file)
		with open(JsonFile,"w") as json_file:
			recipe_dictionary[Recipe_Number][key] = value
			json.dump(recipe_dictionary, json_file, indent=4)
	except:
		print("Single Write Failure")
	
	print(f"Saved: {key}")

#Writes entire recipe to json	
def recipeWrite(Recipe_Info):
	with open(JsonFile,"r") as json_file:
		recipe_dictionary = json.load(json_file)
	with open(JsonFile,"w") as json_file:
		recipe_dictionary[Recipe_Info.SystemNumber] = Recipe_Info.__dict__
		json.dump(recipe_dictionary, json_file, indent=4)
	print(f"Saved: {Recipe_Info.SystemNumber}")


try:
	#Controls are pre-existing loading all stored recipes
	#Loading all recipes is not required. Takes up unneccesary memory
	#Use list method if things get bogged down in the menu via constant json.load()
    #loadControls()
    
    #Load data of last run recipe
    #print("Testing for last run recipe")
    last_recipe=singleLoad(0)
    print(f"Success! Last run Recipe:\n{last_recipe}")
    
    
except:
	#Controls are not pre-existing, creating new recipes
	for i in range (0,6):
		new_recipe = Recipe(SystemNumber=i)
		recipe_list.append(new_recipe)
	print('Initial Load\nNo System Information Saved\nCreating New Data\n')	
	writeControls()
	
  
  
#Test field
#All Below are successful  
#try:
	#recipe_list = loadControls()
	#print(recipe_list[0].SystemNumber)
	#singleWrite(10, "P_pump_ml", 777)
	#Test_Recipe = Recipe(10)
	#Test_Recipe.P_pump_tune=1
	#recipeWrite(Test_Recipe)
	
#except:
	#print("Failure for singlewrite")
