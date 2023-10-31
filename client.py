

import argparse


def main():

    
    pass




if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Client script for sending CSV data to the server.")
    parser.add_argument("-f", "--csv-file", required=True, help="Input CSV file")
    parser.add_argument("-k", "--keys", nargs='+', help="Additional columns to include in the Excel file")
    parser.add_argument("-c", "--colored", action="store_true", help="Color rows based on hu age")
    args = parser.parse_args()

    print("Parsed arguments:")
    print(f"Keys: {args.keys}")
    print(f"Colored: {args.colored}")

    main()