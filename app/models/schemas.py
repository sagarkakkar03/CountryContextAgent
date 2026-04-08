from pydantic import BaseModel, Field
from typing import List



ALLOWED_API_FIELDS = [
    "name", "capital", "population", "currencies", "languages", 
    "region", "subregion", "borders", "area", "flags", 
    "timezones", "continents", "maps"
]


class IntentExtraction(BaseModel):
    """
    Schema for extracting the the fields from user's query.
    """
    countries: List[str] = Field(..., description="The countries the user is asking about.")

    fields: List[str] = Field(..., description="The fields the user is asking about.")
