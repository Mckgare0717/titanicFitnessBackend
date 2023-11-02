from pydantic import BaseModel
import json

class User(BaseModel):
    email: str
    # id:str
    display_name:str
    # password:str
    exercise_plans:list
    diet_plans:list
    access_token:str
    exercise_plans:dict
    
class Creds(BaseModel):
    email:str
    password:str
    display_name:str = None
    
class Token(BaseModel):
    access_token:str
    
class Progress(BaseModel):
    triceps: int
    biceps: int
    forearms:int
    chest:int
    
def getUsersDB(): 
    with open(r"db/userDb.json", "r+") as file: 
        return json.load(file) 
    
def saveUsersDB(newUsers): 
    with open("db/usersDB.json", "w+") as file: 
        file.write(json.dumps(newUsers, indent=4))
        
def getExerciseDB():
    with open("db/exercise.json","r+") as file:
        return json.load(file)

def getWorkoutsDB():
    with open("db/workouts.json","r+") as file:
        return json.load(file)
    
def saveWorkoutsDb(newWorkout):
    with open("db/workouts.json","w+") as file:
        file.write(json.dumps(newWorkout, indent=4))

    