from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from db.schemas import User,getUsersDB,Creds,Token, Progress,saveUsersDB,newUser,getWorkouts,usetoken,delWorkout
import uuid
import jwt


app =FastAPI()
origins = [
    "http://localhost",
    "http://localhost:3000",
    "https://localhost",
    "https://localhost:3000",
    "*"# Assuming your React app runs on port 3000
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
SECRET_KEY = "titanicFitness"

db = getUsersDB()
@app.get("/")
def welcmePg():
    return{"welcome to my page"}

@app.post("/register",response_model=User)
async def register(user: newUser):
    if user.email in db:
        raise HTTPException(status_code=401, detail="User already exists")
    else:
        id =str(uuid.uuid1())
        tokenID = {"sub":id}
        token  = jwt.encode(tokenID,SECRET_KEY,algorithm="HS256")
        
        newUser = {
                    "id":id,
                "email":user.email,
                "password":user.password, 
                "display_name":user.display_name,
                "age":user.age,
                "exercise_plans": [],
                "diet_plans" : [],
                "access_token" : token
                }
        #generate unique access token here and give it to the new user 

        db[user.email] = newUser
        saveUsersDB(db)
        return newUser

# Login route
@app.post("/login", response_model=User)
async def login(user: Creds):
    
    for u in db:
        # print(db[u])
        if db[u]["email"] == user.email and db[u]["password"] == user.password:
            # return {"message": "Login successful"}
            return db[u]
    raise HTTPException(status_code=401, detail="Invalid credentials")

@app.post("/workouts")
async def Workouts(workouts:getWorkouts):
    db = getUsersDB()
    newWorkout={
        "exercise_name":workouts.name,
        "exercise_type":workouts.type,
        "exercise_difficulty":workouts.difficulty,
        "exercise_equipment":workouts.equipment,
        "exercise_instruction":workouts.inst
    }
    for i in db:
        if workouts.access_token  ==  db[i]["access_token"]:
            db[i]["exercise_plans"].append(newWorkout)
            saveUsersDB(db)
            return newWorkout
    raise HTTPException(status_code=401,detail="failed to add workout")


@app.post("/myworkouts")
async def  myWorkouts(token:usetoken):
    db = getUsersDB()
    for i in db:
        if token.access_token  == db[i]["access_token"]:
            if db[i]["exercise_plans"] == []:
                raise HTTPException(status_code=401,detail="no workouts")
            return db[i]["exercise_plans"]
        
@app.delete("/deleteWorkout",response_model=delWorkout)
async def deleteWorkout(delete:delWorkout):
    db = getUsersDB()
    for i in db:   
        if delete.access_token == db[i]["access_token"]: 
            for j in range(len(db[i]["exercise_plans"])): 
                if delete.exercise_name == db[i]["exercise_plans"][j]["exercise_name"]:
                    del db[i]["exercise_plans"][j]
                    saveUsersDB(db)
                    return {"message":f"{delete.exercise_name} deleted successfully"}
                
    raise HTTPException(status_code=401,detail="failed to delete workout")
                
        
        
    



