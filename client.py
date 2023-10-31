

import argparse


def main():


    parser = argparse.ArgumentParser(description='Transmit CSV to REST API and generate Excel')
    parser.add_argument('-k', '--keys', nargs='+', help='Additional columns to include in the Excel file')
    parser.add_argument('-c', '--colored', action='store_true', help='Color rows based on hu age')
    args = parser.parse_args()

    