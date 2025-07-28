from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.v1.ad_routers import router as ad_router
from src.api.v1.imagen_router import router as imagen_router
from src.config import settings

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

# Register API router
app.include_router(ad_router)
app.include_router(imagen_router)