from fastapi import FastAPI
from fastapi.responses import JSONResponse

# Create a FastAPI instance
app = FastAPI()

# Define a simple root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI!"}

# Define an endpoint that accepts a name and returns a personalized greeting
@app.get("/greet/{name}")
def greet(name: str):
    return {"message": f"Hello, {name}!"}

# Define an endpoint that returns a custom JSON response
@app.get("/json")
def custom_json():
    data = {"status": "success", "data": {"key": "value"}}
    return JSONResponse(content=data)
