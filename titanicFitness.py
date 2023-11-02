from fastapi import FastAPI

app =FastAPI()

@app.get("/")
def welcmePg():
    return{"welcome to my page"}