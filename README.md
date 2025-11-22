# How to run
## Clone the repository
`git clone https://github.com/Ali00000007/elanco-task`

## Install dependencies
`pip install -r requirements.txt`

## Run FastAPI server
`uvicorn app:app --reload`

## Accessing API
- Open your browser and go to `http://127.0.0.1:8000/docs`

# Architecture decisions
- I decided to use FastAPI for its simplicity and speed
- The python requests library to fetch the data, because it is lightweight, easy to use and best suited to this task 


# How the system consumes and presents data

## Data fetching
- Each endpoint fetches data from the API via the requests library
- The data is retrieved as JSON

## Data processing 
- The `remove_duplicates` function removes all the duplicates
- It does this by addding the unique ID of each tick sighting to a set if it is not already in the set, and then adding it to a list, otherwise it will skip over that ID

- The `remove_incomplete_entries` function removes all tick sightings that have incomplete infromation

- Both of these functions are called at every API endpoint to ensure that the data returned has no dupplicates and no entries with missing fields

## Presentation
- The API return JSON responses, ready to be consumed by a frontend web application or visualisation tool

# What I could have done better
- Implement more rhobust error handling, currently API faliures return a simple 502 error status
- Currently, each request fetches data from the API, which can be slow or fail. I could implement caching to reduce API calls and improve response time

