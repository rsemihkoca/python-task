from fastapi import FastAPI, File, UploadFile, Form, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import requests
import pandas as pd
import csv, io, httpx

app = FastAPI()

access_token = ""
merged_data = []

class RequestData(BaseModel):
    file: UploadFile = File(...)  # The UploadFile parameter is defined correctly
    keys: str = Form(...)
    colored: bool = Form(True)

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


async def fetch_vehicle_resources(access_token: str):
    async with httpx.AsyncClient() as client:
        url = "https://api.baubuddy.de/dev/index.php/v1/vehicles/select/active"
        headers = {"Authorization": f"Bearer {access_token}"}
        response = await client.get(url, headers=headers)
        if response.status_code != 200:
            return {"error": "Failed to fetch vehicle data"}

        vehicle_data = response.json()

        if len(vehicle_data) == 0:
            return None
        return vehicle_data

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/process_csv")
async def process_csv(request_data: RequestData,  # Use request_data parameter to access RequestData model
                      access_token: str = Depends(get_access_token)):
    
    # Read the CSV file
    try:
        if not file.filename.endswith('.csv'):
            raise HTTPException(status_code=400, detail="Invalid file format. Please upload a CSV file.")
        
        data = await file.read()

        # Parse the CSV data
        csv_data = []
        try:
            csv_data = list(csv.reader(data.decode().splitlines()))
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error parsing CSV file: {str(e)}")

        # Fetch vehicle resources from the API
        vehicle_resources = await fetch_vehicle_resources(access_token)

        if vehicle_resources is None:
            return JSONResponse(content={"error": "Failed to fetch vehicle data"}, status_code=500)
 
        # Merge the CSV data with the fetched resources and apply filtering
        merged_data.clear()
        for row in csv_data[1:]:  # Skip the header row
            vehicle_id = row[0]
            for vehicle in vehicle_resources:
                if vehicle_id == str(vehicle["id"]) and vehicle.get("hu"):
                    label_colors = await resolve_label_color(vehicle["labelIds"])
                    merged_data.append({
                        "id": vehicle["id"],
                        "hu": vehicle["hu"],
                        "labelColors": label_colors
                    })

        response_data =  {"merged_data": merged_data}

        return JSONResponse(content=response_data)

    except Exception as e:
        error_message = str(e)
        return JSONResponse(content={"error": error_message}, status_code=500)




if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)