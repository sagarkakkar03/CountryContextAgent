from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import StreamingResponse
from app.agent.graph import graph
from app.core.logger import logger
from app.core.exceptions import global_exception_handler
import time
import json

app = FastAPI(title="Country Information Agent API")

# Register our custom global exception handler
app.add_exception_handler(Exception, global_exception_handler)

@app.middleware("http")
async def log_requests_middleware(request: Request, call_next):
    """
    Middleware that intercepts every incoming request.
    Logs structured data about the request and response.
    """
    start_time = time.time()
    
    # Extract useful request data
    client_ip = request.client.host if request.client else "unknown"
    method = request.method
    url = str(request.url)
    
    # Log the incoming request with extra structured data
    logger.info(
        f"Incoming request: {method} {url}",
        extra={
            "http_method": method,
            "url": url,
            "client_ip": client_ip,
            "event": "request_started"
        }
    )
    
    # Process the request
    response = await call_next(request)
    
    # Calculate execution time
    process_time = time.time() - start_time
    
    # Log the completion with structured data
    logger.info(
        f"Request completed: {response.status_code} in {process_time:.4f}s",
        extra={
            "http_method": method,
            "url": url,
            "status_code": response.status_code,
            "process_time_seconds": round(process_time, 4),
            "event": "request_completed"
        }
    )
    
    return response

@app.post("/")
async def query(query: str):
    """
    Invoke the agentic workflow to answer user's query.
    """
    if not query or not query.strip():
        logger.warning(
            "User attempted to send an empty query.",
            extra={"event": "validation_failed", "reason": "empty_query"}
        )
        raise HTTPException(status_code=400, detail="Query cannot be empty.")
        
    logger.info(
        f"Processing query: '{query}'",
        extra={"event": "agent_started", "user_query": query}
    )
    
    result = await graph.ainvoke({"query": query})
    
    logger.info(
        "Successfully generated answer.",
        extra={
            "event": "agent_finished", 
            "user_query": query,
            "final_answer": result["final_answer"]
        }
    )
    
    return result["final_answer"]

@app.get("/stream")
async def stream_query(query: str):
    """
    Stream the agent workflow steps as Server-Sent Events (SSE).
    This allows the UI to show real-time progress of each agent node.
    """
    if not query or not query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty.")

    async def event_generator():
        try:
            async for event in graph.astream({"query": query}):
                for node_name, node_state in event.items():
                    # We send each node's output as a JSON string
                    data = {
                        "node": node_name,
                        "state": node_state
                    }
                    yield f"data: {json.dumps(data)}\n\n"
        except Exception as e:
            error_data = {"error": str(e)}
            yield f"data: {json.dumps(error_data)}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")
