from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from db.schemas import User,getUsersDB


app =FastAPI()
origins = [
    "http://localhost",
    "http://localhost:3000",  # Assuming your React app runs on port 3000
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

@app.post("/register")
async def register(user: User):
    db.append(user)
    return {"message": "User registered successfully"}

# Login route
@app.post("/login")
async def login(user: User):
    for u in db:
        if u.email == user.email and u.password == user.password:
            return {"message": "Login successful"}
    raise HTTPException(status_code=401, detail="Invalid credentials")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)