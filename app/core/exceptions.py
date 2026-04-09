from fastapi import Request
from fastapi.responses import JSONResponse
from app.core.logger import logger

async def global_exception_handler(request: Request, exc: Exception):
    """
    Catches any unhandled exceptions in the app, logs the full error trace to our file,
    and returns a clean 500 Internal Server Error to the user instead of crashing.
    """

    logger.error(f"Unhandled exception on {request.url}: {exc}", exc_info=True)
    
    return JSONResponse(
        status_code=500,
        content={"detail": "An internal server error occurred. Please try again later."},
    )
