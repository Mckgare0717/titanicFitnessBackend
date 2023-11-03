from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from db.schemas import User,getUsersDB,Creds,Token, Progress,saveUsersDB,newUser


app =FastAPI()
origins = [
    "http://localhost",
    "http://localhost:3000",
    "https://localhost",
    "https://localhost:3000"# Assuming your React app runs on port 3000
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


db = getUsersDB()
@app.get("/")
def welcmePg():
    return{"welcome to my page"}

@app.post("/register",response_model=User)
async def register(user: newUser):
    newUser = {
               "email":user.email,
               "password":user.password, 
               "display_name":user.display_name,
               "age":user.age,
               "exercise_plans": [],
               "diet_plans" : [],
               "access_token" : ""
               }
    #generate unique access token here and give it to the new user 

    db[user.email] = newUser
    saveUsersDB(db)
    return newUser

# Login route
@app.post("/login", response_model=User)
async def login(user: Creds):
    print(db)
    for u in db:
        # print(db[u])
        if db[u]["email"] == user.email and db[u]["password"] == user.password:
            # return {"message": "Login successful"}
            return db[u]
    raise HTTPException(status_code=401, detail="Invalid credentials")

# @app.get("/progress", response_model=Progress)
# async def progress(token:Token):
    
#     #go through the db to find which user the token belongs to
#     #if not found, do an https exception
    
#     #if found, return the progress from the user you found
    
#     for u in db:
#         for i  in db[u]["exercise_plans"]:
#             print(db[u]["exercise_plans"])
#             return db[u]["exercise_plans"]
        

