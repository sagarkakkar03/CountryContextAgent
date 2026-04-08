import streamlit as st
import requests
import json
import os

st.set_page_config(
    page_title="Country Information Agent",
    layout="centered"
)

st.title("Country Information Agent")
st.write("Ask a question about any country, and watch the AI agents work in real-time!")

def call_agent_api_stream(query: str):
    # Pointing to your deployed Cloud Run backend service
    api_url = os.getenv("API_URL", "https://country-api-208082950137.us-central1.run.app/stream")
    
    st.subheader("Agent Workflow")
    
    step1_placeholder = st.empty()
    step2_placeholder = st.empty()
    step3_placeholder = st.empty()
    
    step1_placeholder.info("1. Intent Agent: Waiting...")
    step2_placeholder.info("2. Search Tool: Waiting...")
    step3_placeholder.info("3. Synthesize Agent: Waiting...")
    
    try:
        response = requests.get(api_url, params={"query": query}, stream=True)
        
        if response.status_code == 200:
            for line in response.iter_lines():
                if line:
                    decoded_line = line.decode('utf-8')
                    if decoded_line.startswith("data: "):
                        data_str = decoded_line[6:]
                        try:
                            event_data = json.loads(data_str)
                            
                            if "error" in event_data:
                                st.error(f"Error from agent: {event_data['error']}")
                                break
                                
                            node_name = event_data.get("node")
                            node_state = event_data.get("state", {})
                            
                            if node_name == "identify_intent":
                                countries = node_state.get('countries', [])
                                fields = node_state.get('fields', [])
                                step1_placeholder.success(f"1. Intent Agent: Extracted Countries: `{countries}` | Fields: `{fields}`")
                                step2_placeholder.warning("2. Search Tool: Fetching data from REST API...")
                            
                            elif node_name == "invoke_search_tool":
                                step2_placeholder.success("2. Search Tool: Data fetched successfully!")
                                
                                with st.expander("View Raw API Data"):
                                    st.json(node_state.get("api_responses", []))
                                    
                                step3_placeholder.warning("3. Synthesize Agent: Crafting final response...")
                            
                            elif node_name == "synthesize_answer":
                                step3_placeholder.success("3. Synthesize Agent: Done!")
                                
                                st.divider()
                                st.subheader("Final Answer")
                                st.write(node_state.get("final_answer"))
                                
                        except json.JSONDecodeError:
                            pass 
        else:
            st.error(f"API Error: {response.status_code} - {response.text}")
            
    except requests.exceptions.ConnectionError:
        st.error("Could not connect to the backend API. Please make sure the FastAPI server is running.")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

query = st.text_input("Your Question:", placeholder="e.g., What is the capital and population of France?")

if st.button("Ask Agent", type="primary"):
    if query.strip():
        call_agent_api_stream(query)
    else:
        st.warning("Please enter a question first!")