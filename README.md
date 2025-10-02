A simple FastAPI application to serve data on upcoming lunar and solar eclipses.

 ## Live Demo
 - Hosted on Render: [https://eclipses-api.onrender.com](https://eclipses-api.onrender.com)
 - API Docs: [https://eclipses-api.onrender.com/docs](https://eclipses-api.onrender.com/docs)

 ## Setup
 1. Install Python 3.10+.
 2. Create a virtual environment: `python -m venv venv`
 3. Activate it: `venv\Scripts\activate` (Windows)
 4. Install dependencies: `pip install -r requirements.txt`
 5. Place `eclipse_data.csv` in the project root.
 6. Run the app: `uvicorn main:app --reload`
 7. Access at `http://localhost:8000` and docs at `http://localhost:8000/docs`.

 ## Endpoints
 - `GET /`: Welcome message with link to docs.
 - `GET /eclipses`: List all eclipses from `eclipse_data.csv`.
 - `GET /eclipses/next`: Get the next upcoming eclipse.
 - `GET /eclipses/{type}`: Filter by type (solar or lunar).

 ## Example Usage
 ```bash
 curl https://eclipses-api.onrender.com/eclipses/next
 ```
 **Response**:
 ```json
 {
   "date": "2025-03-14",
   "type": "lunar",
   "visibility": "Pacific, Americas, Western Europe, Western Africa",
   "duration": 218
 }
 ```

 ## Data Source
 Eclipse data sourced from NASA's catalog (2021–2040), stored in `eclipse_data.csv`.