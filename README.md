# Solution

## Important notes


Since vehicles.csv do not contain hu column only the ones have valid resolved color codes will be colored.

![Alt text](assets/image-1.png)

### Client
1) Creates the name for the future excel file;
2) Analyzes csv file;
3) Sends post request with csv data to server and recieves merged data as response;
4) Analyzes its own running parameters as `-k/--keys` and `-c/--colored`
5) Creates excel file with columns which were called as -k parameters and fills the file with merged data. If there ware not `-k` parameters, it takes all the fields of dictionaries in responce.
6) Colors the cells and font according to the task

### Server
1) Recieves csv data from client;
2) Sends post request to authorization endpoint and recieves a token
3) Using the token sends get request to main endpoint and recieves data
4) Merges data from csv and data from responce
5) Filters out any resources that do not have a value set for `hu` field
6) Returns the result to client

## Running program
1) Clone repository:
```
$ git clone git@github.com:GoodLifeSeeker/python-task.git
```
2) Install and activate virtual environment:
```
- For Mac or Linux:
$ python3 -m venv venv
$ source venv/bin/activate

- For Windows
$ python -m venv venv
$ source venv/Scripts/activate 
``` 
3) Install dependencies from requirements.txt.
```
$ pip install -r requirements.txt
```
4) Run server.py
```
$ python server.py
(If 'python' command doesn't work, use 'python3')
```

5) Open another terminal and run client.py
```
$ python client.py
(If 'python' command doesn't work, use 'python3')
```
6) You can find excel file in the root folder of the project



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