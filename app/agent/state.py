from pydantic import BaseModel, Field
from typing import List, Dict, Any


class AgentState(BaseModel):
    """
    State for the agent.
    """
    query: str = Field(..., description="The user's query.")
    countries: List[str] = Field(default=[], description="The countries that the user is asking about.")
    fields: List[str] = Field(default=[], description="The fields the user is asking about.")
    api_responses: List[Dict[str, Any]] = Field(default=[], description="The API responses.")
    final_answer: str = Field(default="", description="The final answer to the user's query.")
