

import argparse


def main():


    parser = argparse.ArgumentParser(description='Transmit CSV to REST API and generate Excel')
    parser.add_argument('-k', '--keys', nargs='+', help='Additional columns to include in the Excel file')
    parser.add_argument('-c', '--colored', action='store_true', help='Color rows based on hu age')
    args = parser.parse_args()

    print("Parsed arguments:")
    print(f"Keys: {args.keys}")
    print(f"Colored: {args.colored}")

if __name__ == '__main__':
    main()