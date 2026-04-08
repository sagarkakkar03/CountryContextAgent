import httpx
from typing import List, Dict, Any, Optional


async def fetch_country_data(country_name: str, fields: Optional[List[str]] = None) -> List[Dict[str, Any]]:
    """
    Fetches data for a specific country from the REST Countries API.
    """
    url = f"https://restcountries.com/v3.1/name/{country_name}"

    if fields:
        fields_string = ",".join(fields)
        url = f"{url}?fields={fields_string}"

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, timeout=10.0)

            if response.status_code == 404:
                return [{"error": f"Country '{country_name}' not found."}]

            response.raise_for_status()
            return response.json()

        except httpx.RequestError as e:
            return [{"error": f"An error occurred while requesting data: {str(e)}"}]
