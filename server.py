from fastapi import FastAPI, File, UploadFile, Form, Depends, JSONResponse, HTTPException
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


def fetch_vehicle_data(access_token: str):
    # Request vehicle data
    vehicle_data_url = "https://api.baubuddy.de/dev/index.php/v1/vehicles/select/active"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(vehicle_data_url, headers=headers)
    if response.status_code != 200:
        return {"error": "Failed to fetch vehicle data"}

    vehicle_data = response.json()

    if vehicle_data.get("error"):
        return None

    return vehicle_data

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
    try:
        content = TextIOWrapper(file.file, encoding='utf-8')
        df = pd.read_csv(content, engine='python')

        vehicle_data = fetch_vehicle_data(access_token)
        
        if vehicle_data is None:
            return JSONResponse(content={"error": "Failed to fetch vehicle data"}, status_code=500)





        response_data = {}  # Your processed data
        return JSONResponse(content=response_data)

    except Exception as e:
        error_message = str(e)
        return JSONResponse(content={"error": error_message}, status_code=500)




if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)