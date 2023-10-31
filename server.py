from fastapi import FastAPI, File, UploadFile, Form, Depends, HTTPException
import requests
from io import TextIOWrapper
import pandas as pd


app = FastAPI()

access_token = ""
# Function to authenticate and get an access token
def get_access_token():
    global access_token
    LOGIN_URL = "https://api.baubuddy.de/index.php/login"
    HEADERS = {
        "Authorization": "Basic QVBJX0V4cGxvcmVyOjEyMzQ1NmlzQUxhbWVQYXNz",
        "Content-Type": "application/json"
    }
    PAYLOAD = {
        "username": "365",
        "password": "1"
    }
    response = requests.post(LOGIN_URL, json=PAYLOAD, headers=HEADERS)
    if response.status_code == 200:
        access_token = response.json().get("oauth", {}).get("access_token")
        return access_token
    else:
        raise HTTPException(status_code=401, detail="Authentication failed")


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/process_csv")
async def process_csv(
    file: UploadFile = File(...),
    keys: str = Form(...),
    colored: bool = Form(True),
    access_token: str = Depends(get_access_token)
    ):
    
    # Read the CSV file
    content = TextIOWrapper(file.file, encoding='utf-8')
    df = pd.read_csv(content)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)