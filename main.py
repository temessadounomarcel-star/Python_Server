
import uvicorn as uv
from fastapi import FastAPI 
from config import settings
from route.home_routes import router as home_router

app = FastAPI(title=settings.app_name)

app.include_router(home_router,tags=["Home"], prefix="/home")




if __name__ == "__main__":
    uv.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.app_env == "development"
    )