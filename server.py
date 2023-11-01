from fastapi import FastAPI, File, UploadFile, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
import requests
import pandas as pd
import io, httpx

app = FastAPI()

access_token = ""
merged_data = []

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


async def resolve_label_color(access_token: str, labelId):
    async with httpx.AsyncClient() as client:
        url = f"https://api.baubuddy.de/dev/index.php/v1/labels/{labelId}"
        headers = {"Authorization": f"Bearer {access_token}"}
        response = await client.get(url=url, headers=headers)
        return response.json()[0].get("colorCode")

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
async def process_csv(
    file: UploadFile = File(...),
    # keys: str = Form(...),
    # colored: bool = Form(True),
    access_token: str = Depends(get_access_token)
):
    
    # Read the CSV file
    try:
        if not file.filename.endswith('.csv'):
            raise HTTPException(status_code=400, detail="Invalid file format. Please upload a CSV file.")
        
        data = await file.read()

        try:
            csv_data = pd.read_csv(io.BytesIO(data), engine="python", sep=";")
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error parsing CSV file: {str(e)}")
        
        # Fetch vehicle resources from the API
        vehicle_resources = await fetch_vehicle_resources(access_token)

        if vehicle_resources is None:
            return JSONResponse(content={"error": "Failed to fetch vehicle data"}, status_code=500)
 
        # Filter vehicle_resources with 'hu' field not csv_data
        filtered_external_data = pd.DataFrame(vehicle_resources).dropna(subset=["hu"])

        # Remove duplicates and merge according to gruppe	kurzname	langtext	info	lagerort	labelIds
        merged_data = pd.concat([csv_data, filtered_external_data], ignore_index=True)

        # Resolve colorCode for labelIds using async functions
        labelId_color_map = {}
        for labelId in merged_data['labelIds']:
            if pd.notna(labelId) and labelId is not None:
                if isinstance(labelId, (int, float)):
                    colorCode = await resolve_label_color(access_token, int(labelId))
                    labelId_color_map[labelId] = colorCode

        # Map colorCode to the merged_data
        merged_data['colorCode'] = merged_data['labelIds'].map(labelId_color_map)

        # Convert the result to JSON format
        result_json = merged_data.to_json(orient="records")

        return JSONResponse(content=result_json, status_code=200)


    except Exception as e:
        error_message = str(e)
        return JSONResponse(content={"error": error_message}, status_code=500)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)