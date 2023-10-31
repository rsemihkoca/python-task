from datetime import datetime
import pandas as pd
import argparse
import requests

API_ENDPOINT = "localhost:8000/process_csv"

def main(csv_filename:str, keys:str, colored:str)->None:

    # Prepare the request payload
    data = {
        "keys": keys,
        "colored": colored
    }

    # Send a POST request to the server
    response = requests.post(API_ENDPOINT, data=data, files={"file": (csv_filename, open(csv_filename, "rb"))})

    if response.status_code == 200:
        # Process the response JSON data

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
    parser.add_argument("-c", "--colored", action="store_true", help="Color rows based on hu age")
    args = parser.parse_args()

    print("Parsed arguments:")
    print(f"CSV file: {args.csv_file}")
    print(f"Keys: {args.keys}")
    print(f"Colored: {args.colored}")

    main(args.csv_file, args.keys, args.colored)
