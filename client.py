from openpyxl import Workbook
from openpyxl.styles import PatternFill
from datetime import datetime, timedelta
import pandas as pd
import argparse
import requests
import httpx
import asyncio

API_ENDPOINT = "http://0.0.0.0:8000/process_csv"

# Function to determine cell background color based on 'hu' value
def get_cell_color(hu):
    today = datetime.today()
    if hu < today - timedelta(days=90):
        return PatternFill(start_color="007500", end_color="007500", fill_type="solid")  # Green
    elif hu < today - timedelta(days=365):
        return PatternFill(start_color="FFA500", end_color="FFA500", fill_type="solid")  # Orange
    else:
        return PatternFill(start_color="b30000", end_color="b30000", fill_type="solid")  # Red

async def main(file_path:str, keys:str, colored:str)->None:
    async with httpx.AsyncClient(timeout=100) as client:

        with open(file_path, "rb") as file:
            files = {"file": (file_path, file)}

            # Send a POST request to the server
            response = await client.post(API_ENDPOINT, files=files) #, data=data)

        # Check if the response status code is successful
        if response.status_code == 200:
            server_data = response.json()

            # Sort by 'gruppe' field
            server_data.sort(key=lambda x: x['gruppe'])

            # Add 'rnr' column
            keys = set(keys) | {'rnr'}

            # Create an Excel file with the processed data
            current_date = datetime.now().isoformat()
            excel_file_name = f"vehicles_{current_date}.xlsx"

            # Save the Excel file

            print(f"Excel file '{excel_file_name}' saved.")
        else:
            print(f"Server returned an error: {response.status_code}")


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Client script for sending CSV data to the server.")
    parser.add_argument("-f", "--csv-file", required=True, help="Input CSV file")
    parser.add_argument("-k", "--keys", nargs='+', help="Additional columns to include in the Excel file")
    parser.add_argument("-c", "--colored", action="store_false", help="Color rows based on hu age")
    args = parser.parse_args()

    print("Parsed arguments:")
    print(f"CSV file: {args.csv_file}")
    print(f"Keys: {args.keys}")
    print(f"Colored: {args.colored}")


    asyncio.run(main(args.csv_file, args.keys, args.colored))