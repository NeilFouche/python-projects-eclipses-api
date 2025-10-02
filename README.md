# Lunar and Solar Eclipses API

A simple FastAPI application to serve data on upcoming lunar and solar eclipses.

## Setup
1. Install Python 3.10+.
2. Create a virtual environment: `python -m venv venv` or `pipenv shell`
3. Activate it: `venv\Scripts\activate` (Windows)
4. Install dependencies: `pip install -r requirements.txt`
5. Run the app: `uvicorn main:app --reload`
6. Access at `http://localhost:8000` and docs at `http://localhost:8000/docs`.

## Endpoints
- `GET /eclipses`: List all eclipses.
- `GET /eclipses/next`: Get the next upcoming eclipse.
- `GET /eclipses/{type}`: Filter by type (solar or lunar).

## Deployment
- Push to GitHub.
- Deploy on Render using the free tier.

## Data Source
Hardcoded dataset from NASA's eclipse catalog (simplified for MVP).