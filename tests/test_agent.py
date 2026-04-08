import pytest
from app.agent.state import AgentState
from app.agent.nodes.search_tool import invoke_search_tool

@pytest.mark.asyncio
async def test_invoke_search_tool_single_country():
    """
    Test that the search tool node correctly fetches data for one country.
    """
    dummy_state = AgentState(
        query="What is the capital of Japan?",
        countries=["Japan"],
        fields=["capital"]
    )
    result = await invoke_search_tool(dummy_state)
    assert "api_responses" in result
    responses = result["api_responses"]
    assert len(responses) == 1
    assert responses[0]["Japan"][0]["capital"][0] == "Tokyo"

@pytest.mark.asyncio
async def test_invoke_search_tool_multiple_countries():
    """
    EDGE CASE: User asks about multiple countries at once.
    """
    dummy_state = AgentState(
        query="Compare the population of India and China",
        countries=["India", "China"],
        fields=["population"]
    )
    result = await invoke_search_tool(dummy_state)
    responses = result["api_responses"]
    
    # We should get exactly 2 responses back
    assert len(responses) == 2
    
    # Extract the keys (country names) from the list of dicts
    keys = [list(r.keys())[0] for r in responses]
    assert "India" in keys
    assert "China" in keys

@pytest.mark.asyncio
async def test_invoke_search_tool_empty_countries():
    """
    EDGE CASE: LLM found no countries in the query (e.g., greeting).
    """
    dummy_state = AgentState(
        query="Hello, how are you?",
        countries=[],
        fields=[]
    )
    result = await invoke_search_tool(dummy_state)
    assert "api_responses" in result
    # Should return an empty list without crashing
    assert len(result["api_responses"]) == 0
