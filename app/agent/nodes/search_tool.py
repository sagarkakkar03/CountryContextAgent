import asyncio
from app.agent.state import AgentState
from app.tools.countries_api import fetch_country_data


async def invoke_search_tool(state: AgentState) -> dict:
    """
    Invoke the search tool to fetch the data for the given country based on fields the user requested.
    """
    # Fetch data for all countries concurrently
    tasks = [fetch_country_data(country, state.fields) for country in state.countries]
    results = await asyncio.gather(*tasks)

    all_responses = []
    for country, response in zip(state.countries, results):
        all_responses.append({country: response})
        
    return {
        'api_responses': all_responses
    }
