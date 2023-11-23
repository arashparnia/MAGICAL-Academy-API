from fastapi import FastAPI, HTTPException, Body, APIRouter, Depends, status,Request
from fastapi.security.api_key import APIKeyHeader, APIKeyCookie, APIKeyQuery
from ApiKey import get_api_key
from routers.Completion import completion_router
from routers.Audio import audio_router
from routers.Assitant import assistant_router
from routers.GPT4All import gpt4all_router
from APILogger import APILogger
from block_path import blocked_paths
# Initialize FastAPI app without global dependencies
app = FastAPI()

# Include your routers with the API key dependency
app.include_router(completion_router, prefix="/completion", tags=["Completion"], dependencies=[Depends(get_api_key)])
app.include_router(audio_router, prefix="/audio", tags=["Audio"], dependencies=[Depends(get_api_key)])
app.include_router(assistant_router, prefix="/assistant", tags=["Assistant"], dependencies=[Depends(get_api_key)])
app.include_router(gpt4all_router, prefix="/gpt4all", tags=["gpt4all"], dependencies=[Depends(get_api_key)])

app_logger = APILogger("app")
@app.middleware("http")
async def log_requests(request: Request, call_next):
    return await app_logger.log_request(request, call_next)




@app.middleware("http")
async def block_404_requests(request: Request, call_next):
    if request.url.path in blocked_paths:
        raise HTTPException(status_code=403, detail="Forbidden")
    response = await call_next(request)
    return response


# Health Check Endpoint (no API key required)
@app.get("/")
def health_check():
    return {"status": "healthy"}

# Main function to run the app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)