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

@app.get("/", response_model=Eclipse)
async def home():
    return find_next_eclipse()


@app.get("/eclipses", response_model=List[Eclipse])
async def get_all_eclipses():
    return get_eclipses()

@app.get("/eclipses/next", response_model=Eclipse)
async def get_next_eclipse():
    next_eclipse = find_next_eclipse()
    if next_eclipse:
        return next_eclipse

    raise HTTPException(status_code=404, detail="No upcoming eclipses found.")

@app.get("/eclipses/{eclipse_type}", response_model=List[Eclipse])
async def get_eclipses_by_type(eclipse_type: str):
    eclipse_type = eclipse_type.lower()

    if eclipse_type not in ['solar', 'lunar']:
        raise HTTPException(status_code=400, detail="Invalid type. Use 'solar' or 'lunar'.")

    eclipses = get_eclipses(eclipse_type)
    if not eclipses:
        HTTPException(status_code=404, detail=f"No {eclipse_type} eclipses found.")

    return eclipses

def find_next_eclipse():
    now = datetime.now().date()
    eclipses = get_eclipses()
    for eclipse in eclipses:
        eclipse_date = eclipse['date']
        if eclipse_date >= now:
            return eclipse
    return None

def get_eclipses(eclipse_type: Optional[str] = None):
    df = pd.read_csv("eclipse_data.csv", delimiter=";")
    df['date'] = pd.to_datetime(df['date'], errors='coerce').dt.date
    eclipses_df = df[['date', 'type', 'regions', 'duration_sec']]

    if eclipse_type:
        eclipses_df = eclipses_df[eclipses_df['type'].str.contains(eclipse_type, case=False, na=False)]

    return eclipses_df.to_dict('records')
