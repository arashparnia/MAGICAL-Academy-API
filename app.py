from fastapi import  HTTPException, Depends
import logging


from APILogger import APILogger
from ApiKey import get_api_key
from routers.Content import content_router
from routers.Completion import completion_router
from routers.Audio import audio_router
from routers.Assitant import assistant_router
from routers.GoogleGenerativeAI import  GoogleGenerativeAI_router
from block_path import blocked_paths
from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')
app = FastAPI()
# Serve static files from /site/
app.mount("/site", StaticFiles(directory="static", html=True), name="static")


# Redirect to the static site's index.html
@app.get("/")
async def redirect_to_site():
    return RedirectResponse(url="/site/index.html")
# Health Check Endpoint (no API key required)
@app.get("/health")
def health_check():
    return {"status": "healthy"}


# Include your routers with the API key dependency
app.include_router(content_router, prefix="/content", tags=["Content"], dependencies=[Depends(get_api_key)])
app.include_router(completion_router, prefix="/completion", tags=["Completion"], dependencies=[Depends(get_api_key)])
app.include_router(audio_router, prefix="/audio", tags=["Audio"], dependencies=[Depends(get_api_key)])
app.include_router(assistant_router, prefix="/assistant", tags=["Assistant"], dependencies=[Depends(get_api_key)])
app.include_router(GoogleGenerativeAI_router, prefix="/GoogleGenerativeAI", tags=["GoogleGenerativeAI"], dependencies=[Depends(get_api_key)])

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





# Main function to run the app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
