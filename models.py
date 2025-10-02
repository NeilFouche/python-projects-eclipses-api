from pydantic import BaseModel
from datetime import date

class Eclipse(BaseModel):
    date: date
    type: str
    regions: str
    duration_sec: int | None = None