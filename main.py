"""
Eclipses API
by Neil Fouche

A simple FastAPI application to serve data on upcoming lunar and solar eclipses.

Host: render.com @ https://eclipses-api.onrender.com
"""

import pandas as pd
from fastapi import FastAPI, HTTPException
from typing import List, Optional
from datetime import datetime
from models import Eclipse

app = FastAPI(
    title="Lunar and Solar Eclipse API",
    description="A simle API for eclipse data"
)

# Load CSV at startup to avoid reading on every request
ECLIPSES_DF = pd.read_csv("eclipse_data.csv", delimiter=";")
ECLIPSES_DF['date'] = pd.to_datetime(ECLIPSES_DF['date'], errors='coerce').dt.date

# Filter out invalid dates
ECLIPSES_DF = ECLIPSES_DF[ECLIPSES_DF['date'].notna()]

@app.get("/", response_model=dict)
async def home():
    """Welcome endpoint for the Eclipses API.

    Returns:
        dict: A welcome message with a link to the API documentation.
    """
    return {"message": "Welcome to the Lunar and Solar Eclipses API", "docs": "/docs"}


@app.get("/eclipses", response_model=List[Eclipse])
async def get_all_eclipses():
    """Retrieve a list of all lunar and solar eclipses from the dataset.

    Returns:
        List[Eclipse]: A list of eclipse objects with date, type, visibility, and duration.
    """
    return get_eclipses()

@app.get("/eclipses/next", response_model=Eclipse)
async def get_next_eclipse():
    """Retrieve the next upcoming eclipse after the current date.

    Returns:
        Eclipse: The next eclipse object with date, type, visibility, and duration.

    Raises:
        HTTPException: 404 if no upcoming eclipses are found.
    """
    next_eclipse = find_next_eclipse()
    if next_eclipse:
        return next_eclipse

    raise HTTPException(status_code=404, detail="No upcoming eclipses found.")

@app.get("/eclipses/{eclipse_type}", response_model=List[Eclipse])
async def get_eclipses_by_type(eclipse_type: str):
    """Retrieve a list of eclipses filtered by type (solar or lunar).

    Args:
        eclipse_type (str): The type of eclipse to filter ("solar" or "lunar").

    Returns:
        List[Eclipse]: A list of eclipse objects matching the specified type.

    Raises:
        HTTPException: 400 if the eclipse type is invalid.
        HTTPException: 404 if no eclipses of the specified type are found.
    """
    eclipse_type = eclipse_type.lower()

    if eclipse_type not in ['solar', 'lunar']:
        raise HTTPException(status_code=400, detail="Invalid type. Use 'solar' or 'lunar'.")

    eclipses = get_eclipses(eclipse_type)
    if not eclipses:
        HTTPException(status_code=404, detail=f"No {eclipse_type} eclipses found.")

    return eclipses

def find_next_eclipse():
    """Find the next eclipse after the current date.

    Returns:
        dict: The next eclipse record, or None if no upcoming eclipses are found.
    """
    now = datetime.now().date()
    eclipses = get_eclipses()
    for eclipse in eclipses:
        if eclipse['date'] >= now:
            return eclipse
    return None

def get_eclipses(eclipse_type: Optional[str] = None):
    """Load and filter eclipse data from the CSV dataset.

    Args:
        eclipse_type (Optional[str]): The type of eclipse to filter ("solar" or "lunar"), or None for all eclipses.

    Returns:
        List[dict]: A list of eclipse records with date, type, visibility, and duration.
    """
    df = ECLIPSES_DF.copy()

    df['type'] = df['type'].str.lower().str.split(' - ').str[0]
    df = df.rename(columns={"duration_sec": "duration"})
    df['duration'] = (df['duration'] / 60).round().astype("Int64")

    if eclipse_type:
        df = df[df['type'].str.contains(eclipse_type, case=False, na=False)]

    return df[['date', 'type', 'regions', 'duration']].to_dict('records')
