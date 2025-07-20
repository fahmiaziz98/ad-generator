import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from api.router import router
from config import settings

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug,
    description="MVP Ad Generator with Database Integration"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this to your needs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    response = await call_next(request)
    process_time = response.headers.get("X-Process-Time")
    if process_time:
        response.headers["X-Process-Time"] = process_time
    return response

app.include_router(router)

# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000, reload="True")
# server/src/main.py
# To run the server, use the command: uvicorn main:app --reload
# This will start the FastAPI server with live reloading enabled.
