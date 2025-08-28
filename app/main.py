from fastapi import FastAPI
from app.api.routes import router as api_router
from app.config import settings

app = FastAPI(title=settings.app_name, debug=settings.debug)

app.include_router(api_router)

@app.get("/")
async def root():
    return {
        "message": f"{settings.app_name} läuft!",
            "environment": settings.app_env
            }
