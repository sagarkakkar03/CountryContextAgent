from langgraph.graph import StateGraph, START, END
from app.agent.nodes.intent import identify_intent
from app.agent.state import AgentState
from app.agent.nodes.search_tool import invoke_search_tool
from app.agent.nodes.synthesize import synthesize_answer

graph = StateGraph(AgentState)
graph.add_node('identify_intent', identify_intent)
graph.add_node('invoke_search_tool', invoke_search_tool)
graph.add_node('synthesize_answer', synthesize_answer)

graph.add_edge(START, 'identify_intent')
graph.add_edge('identify_intent', 'invoke_search_tool')
graph.add_edge('invoke_search_tool', 'synthesize_answer')
graph.add_edge('synthesize_answer', END)
graph =graph.compile()
