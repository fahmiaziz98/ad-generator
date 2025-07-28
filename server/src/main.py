from loguru import logger
from datetime import datetime
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.v1.ad_routers import router as ad_router
from src.api.v1.imagen_router import router as imagen_router
from src.config import settings


logger.add("logger.log", rotation="10 MB", retention="10 days", level="DEBUG")

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
    description=settings.APP_DESCRIPTION,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# add router healthcheck
@app.get("/healthcheck")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": settings.APP_VERSION,
        "service": settings.APP_NAME
    }


# Register API router
app.include_router(ad_router)
app.include_router(imagen_router)