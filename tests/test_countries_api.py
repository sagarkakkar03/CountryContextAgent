import pytest
from app.tools.countries_api import fetch_country_data

@pytest.mark.asyncio
async def test_fetch_country_data_success():
    """
    Test that the API client correctly fetches data for a real country.
    """
    result = await fetch_country_data("Germany", ["capital"])
    assert isinstance(result, list)
    assert result[0]["capital"][0] == "Berlin"

@pytest.mark.asyncio
async def test_fetch_country_data_not_found():
    """
    Test that the API client correctly handles a 404 error for a fake country.
    """
    result = await fetch_country_data("Narnia")
    assert isinstance(result, list)
    assert "error" in result[0]
    assert "not found" in result[0]["error"].lower()

@pytest.mark.asyncio
async def test_fetch_country_data_multiple_words():
    """
    EDGE CASE: Country with spaces in the name.
    """
    result = await fetch_country_data("United States", ["name"])
    assert isinstance(result, list)
    assert "error" not in result[0]
    assert "United States" in result[0]["name"]["common"]

@pytest.mark.asyncio
async def test_fetch_country_data_no_fields():
    """
    EDGE CASE: No specific fields requested (should return full payload).
    """
    result = await fetch_country_data("Brazil")
    assert isinstance(result, list)
    # Check that multiple default fields are present
    assert "capital" in result[0]
    assert "population" in result[0]
    assert "currencies" in result[0]
