from app.agent.state import AgentState
from langchain_openai import ChatOpenAI
from app.core.config import Config

llm = ChatOpenAI(model=Config.OPENAI_MODEL)

async def synthesize_answer(state: AgentState) -> dict:
    """
    This creates a final answer to the user's query based on the API responses and the user's query.
    """
    prompt = f"""
    You are a helpful assistant that answers questions about countries.
    The user's query is: {state.query}
    The API responses are: {state.api_responses}
    Answer the user's question using ONLY the data provided above.
    The final answer should be friendly, concise, and human-readable.
    """

    response = await llm.ainvoke(prompt)
    return {
        'final_answer': response.content
    }
