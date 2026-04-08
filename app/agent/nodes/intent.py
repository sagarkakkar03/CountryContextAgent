from langchain_openai import ChatOpenAI
from app.models.schemas import IntentExtraction
from app.agent.state import AgentState
from app.core.config import Config

llm = ChatOpenAI(model=Config.OPENAI_MODEL).with_structured_output(IntentExtraction)

async def identify_intent(state: AgentState) -> dict:
    """
    Identify the intent of users query and return the countries and fields the user is asking about.
    """
    prompt = f"Extract the countries and data fields from this question: {state.query}"
    llm_response = await llm.ainvoke(prompt)

    return {
        'countries': llm_response.countries,
        'fields': llm_response.fields
    }
