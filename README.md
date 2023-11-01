# Solution

## Important notes


Since vehicles.csv do not contain hu column only the ones have valid resolved color codes will be colored.

![Alt text](assets/image-1.png)


# Server README

## Introduction
This README provides information and instructions for setting up and using the Python server script, which is built with FastAPI and managed using Poetry. The server script is designed to process CSV data sent by the client and return the processed data in JSON format.

## Prerequisites
Before using the server script, make sure you have Poetry installed on your Ubuntu system. You can install Poetry by running the following command:

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

## Installation
1. Clone or download the project directory containing the server script to your local machine. You can use the `git clone` command or download the repository as a ZIP file from the repository's web page.

```bash
git clone https://github.com/rsemihkoca/python-task
```

2. Navigate to the project directory using the `cd` command:

```bash
cd repo
```

3. Install the required dependencies using Poetry:

```bash
poetry install
```

4. Activate shell with Poetry:

```bash
poetry shell
```
## Usage
To use the server script, follow these steps:

1. Open a terminal.

2. Navigate to the project directory.

3. Run the server script using Poetry:

```bash
poetry run python server.py
```

4. The server will start and listen on `http://0.0.0.0:8000`. It is ready to receive POST requests with CSV data for processing.

5. Ensure the client script is configured to send data to the correct API endpoint (`API_ENDPOINT` in the client script).

## API Endpoint
The server listens on the following API endpoint:

- `http://0.0.0.0:8000/process_csv`

## Sample Output
The server script processes the received CSV data and returns it in JSON format. The client script will then use this data to generate an Excel file.

**Client README**

# Client README

## Introduction
This README provides information and instructions for using the Python client script, which is responsible for sending CSV data to a server and generating an Excel file with the received data. The client script is managed and run using Poetry.

## Prerequisites
Before using the client script, make sure you have Poetry installed on your Ubuntu system. You can install Poetry by running the following command:

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

## Installation
1. Clone or download the project directory containing the client script to your local machine. You can use the `git clone` command or download the repository as a ZIP file from the repository's web page.

```bash
git clone https://github.com/your/repo.git
```

2. Navigate to the project directory using the `cd` command:

```bash
cd repo
```

3. Install the required dependencies using Poetry:

```bash
poetry install
```

## Usage
To use the client script, follow these steps:

1. Open a terminal.

2. Navigate to the directory where the client script is located.

3. Run the client script using Poetry with the required arguments. You can use the following command:

```bash
poetry run python client.py -f CSV_FILE_PATH [-k KEY [KEY ...]] [-c]
```

Replace the following placeholders:
- `CSV_FILE_PATH` with the path to your input CSV file.
- `KEY` with additional column names to include in the generated Excel file.
- `-c` to enable row coloring based on `hu` age (optional).

Example usages:

- Basic usage without additional keys or row coloring:
  ```bash
  poetry run python client.py -f input.csv
  ```

- Including additional keys in the Excel file:
  ```bash
  poetry run python client.py -f input.csv -k column1 column2
  ```

- Enabling row coloring based on `hu` age:
  ```bash
  poetry run python client.py -f input.csv -c
  ```

4. The client script will send a POST request to the server specified in `API_ENDPOINT`. It will receive the data in response, generate an Excel file, and save it with a timestamp in the filename.

5. The generated Excel file will be saved in the same directory as the client script.

## Arguments
- `-f`, `--csv-file`: Required. The path to the input CSV file to be sent to the server.
- `-k`, `--keys`: Optional. Additional column names to include in the Excel file. Provide one or more column names as arguments separated by spaces.
- `-c`, `--colored`: Optional. Enable row coloring based on `hu` age. If this flag is included, rows will be colored in the Excel file.

## Sample Output
The client script will generate an Excel file in the same directory as the script. The filename will include a timestamp in ISO format. For example, `vehicles_2023-11-01T10-30-00.xlsx`.
# README

Hello dear python dev!

This repository is supposed to act as a playground for your submission.

Before getting started, please make sure use this repository as a **template** and create your own **public** repository, on which you will commit and push your code regularly. 
Once you are ready, please mail us back the link to your repository. 

Below, you will find the **Task** definition.

Happy Hacking :computer:

# Task

Write two python scripts that have to achieve the common goal to downloads a certain set of resources, merges them with CSV-transmitted resources, and converts them to a formatted excel file.
In particular, the script should:

## Client

Transmits a CSV to a REST-API (s. Server-section below), handles the response and generates an Excel-File taking the input parameters into account.

- Take an input parameter `-k/--keys` that can receive an arbitrary amount of string arguments
- Take an input parameter `-c/--colored` that receives a boolean flag and defaults to `True`

- Transmit CSV containing vehicle information to the POST Call of the server (example data: [vehicles.csv](vehicles.csv))
- Convert the servers response into an excel file that contains all resources and make sure that:
   - Rows are sorted by response field `gruppe`
   - Columns always contain `rnr` field
   - Only keys that match the input arguments are considered as additional columns (i.e. when the script is invoked with `kurzname` and `info`, print two extra columns)
   - If `labelIds` are given and at least one `colorCode` could be resolved, use the first `colorCode` to tint the cell's text (if `labelIds` is given in `-k`)
   - If the `-c` flag is `True`, color each row depending on the following logic:
     - If `hu` is not older than 3 months --> green (`#007500`)
     - If `hu` is not older than 12 months --> orange (`#FFA500`)
     - If `hu` is older than 12 months --> red (`#b30000`)
   - The file should be named `vehicles_{current_date_iso_formatted}.xlsx`

## Server

This script should offer a REST-API, that accepts a CSV, downloads a certain set of resources, merges them with the CSV, applies filtering, and returns them in an appropriate data-structure

- REST-API (e.g. FastAPI, Flask, Django …) offering a POST Call which accepts a transmitted CSV containing vehicle information 
- Upon receiving a valid CSV file, do the following
   - Request the resources located at `https://api.baubuddy.de/dev/index.php/v1/vehicles/select/active`
   - Store both of them (the API Response + request body) in an appropriate data structure and make sure the result is distinct
   - Filter out any resources that do not have a value set for `hu` field
   - For each `labelId` in the vehicle's JSON array `labelIds` resolve its `colorCode` using `https://api.baubuddy.de/dev/index.php/v1/labels/{labelId}`
   - return data-structure in JSON format

### Authorization

It's mandatory for your requests towards the https://api.baubuddy.de to be authorized. You can find the required request below:

This is how it looks in `curl`:

```bash
curl --request POST \
  --url https://api.baubuddy.de/index.php/login \
  --header 'Authorization: Basic QVBJX0V4cGxvcmVyOjEyMzQ1NmlzQUxhbWVQYXNz' \
  --header 'Content-Type: application/json' \
  --data '{
        "username":"365",
        "password":"1"
}'
```

The response will contain a json object, having the access token in `json["oauth"]["access_token"]`. For all subsequent calls this has to be added to the request headers as `Authorization: Bearer {access_token}`.

A possible implementation in `Python` could be the following. You don't have to copy over this one, feel free to indivualize it or use a different network library.

```python
import requests
url = "https://api.baubuddy.de/index.php/login"
payload = {
    "username": "365",
    "password": "1"
}
headers = {
    "Authorization": "Basic QVBJX0V4cGxvcmVyOjEyMzQ1NmlzQUxhbWVQYXNz",
    "Content-Type": "application/json"
}
response = requests.request("POST", url, json=payload, headers=headers)
print(response.text)
```