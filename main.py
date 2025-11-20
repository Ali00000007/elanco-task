from fastapi import FastAPI,HTTPException
import httpx
from datetime import datetime

app = FastAPI()

def remove_duplicates(data):
    seen_ids = set()
    unique_data = []

    for item in data:
        if item["id"] not in seen_ids:
            unique_data.append(item)
            seen_ids.add(item["id"])
    
    return unique_data

def remove_incomplete_entries(data):
    required_fields = ["id", "location", "species", "date"]
    cleaned_data = [item for item in data if all(field in item and item[field] for field in required_fields)]
    return cleaned_data

def parse_date(date_str: str) -> datetime:
    try:
        return datetime.fromisoformat(date_str)
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Invalid date format: {date_str}. Use YYYY-MM-DD or ISO format.")

@app.get("/data/tick-sightings")
async def get_tick_sightings():
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get("https://dev-task.elancoapps.com/data/tick-sightings")
            response.raise_for_status()
        except httpx.HTTPStatusError:
            raise HTTPException(status_code=502, detail="Failed to fetch data from third-party API")

    data = response.json()
    data = remove_incomplete_entries(data)
    data = remove_duplicates(data)
    return data

@app.get("/data/tick-sightings/city/{location}")
async def get_tick_sightings_by_city(location: str):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"https://dev-task.elancoapps.com/data/tick-sightings/city/{location}")  
            response.raise_for_status()
        except httpx.HTTPStatusError:
            raise HTTPException(status_code=502, details="Failed to fetch data from third part API")
    data = response.json()
    data = remove_incomplete_entries(data)
    data = remove_duplicates(data)
    return data
    
@app.get("/data/tick-sightings/species/{species_name}")
async def get_tick_sightings_by_species(species_name: str):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"https://dev-task.elancoapps.com/data/tick-sightings/species/{species_name}")  
            response.raise_for_status()
        except httpx.HTTPStatusError:
            raise HTTPException(status_code=502, details="Failed to fetch data from third part API")
        data = response.json()
        data = remove_incomplete_entries(data)
        data = remove_duplicates(data)
        return data


@app.get("/data/tick-sightings/filter")
async def filter_tick_sightings(
    city: str = None,
    species: str = None,
    start_date: str = None,
    end_date: str = None
):
    async with httpx.AsyncClient() as client:
        response = await client.get("https://dev-task.elancoapps.com/data/tick-sightings")
        response.raise_for_status()
    data = response.json()

    data = remove_incomplete_entries(data)
    data = remove_duplicates(data)

    if city:
        data = [item for item in data if item["location"].lower() == city.lower()]
    if species:
        data = [item for item in data if item["species"].lower() == species.lower()]

    if start_date:
        start = parse_date(start_date)
        data = [item for item in data if datetime.fromisoformat(item["date"]) >= start]

    if end_date:
        end = parse_date(end_date)
        data = [item for item in data if datetime.fromisoformat(item["date"]) <= end]

    if not data:
        raise HTTPException(status_code=404, detail="No sightings found for given filters")

    return data
