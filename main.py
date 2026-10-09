
import uvicorn as uv
from fastapi import FastAPI , Depends, HTTPException


from config import settings
from route.home_routes import router as home_router
from route.user_routes import router as user_router
from route.test import router as test_router


from Config.db import database,Base

app = FastAPI(title=settings.app_name)

#test de la connexion
@app.on_event("startup")
def startup():
    database.connect()
    Base.metadata.create_all(bind=database.engine)



app.include_router(home_router,tags=["Home"], prefix="/home")
app.include_router(user_router,tags=["Users"], prefix="/users")






app.include_router(test_router, tags=["Test"], prefix="/database")
















if __name__ == "__main__":
    uv.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.app_env == "development"
    )