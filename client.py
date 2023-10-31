
import pandas as pd
import argparse


def main(csv_filename:str, keys:str, colored:str)->None:

    # Load the CSV data
    csv_data = pd.read_csv(csv_filename, engine="python")

    # Prepare the request payload
    payload = {
        "data": csv_data.to_dict(orient="records"),
        "keys": keys,
        "colored": colored
    }

    




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
