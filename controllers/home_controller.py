from config import settings
from fastapi import Request, Response
from fastapi.responses import JSONResponse
import json

class HomeController:
    def __init__(self):
        self.settings = settings

    async def accueil(self, req: Request, res: Response):
        params = req.query_params
        message = str(params.get("message", "Aucun message fourni"))
        age = int(params.get("age", "Aucun âge fourni"))

        content={
            "message": "Serveur Fonctionnel",
            "application": self.settings.app_name,
            "environnement": self.settings.app_env,
            "port": self.settings.port,
            "method": req.method,
            "url": str(req.url),
            "values": {
                "message": message,
                "age": age
            }
        }
        res.status_code = 200
        
        return JSONResponse(content=content, status_code=res.status_code)
    
    async def post_message(self, req: Request, res: Response):
        message = await req.form()
        return JSONResponse(
            content={
                "message": "post route is working!", 
                "user_message": message.get("message")
                },
            status_code=200
                )

    async def delete_message(self, req: Request, res: Response):
        return JSONResponse(
            content={
                "message": "delete route is working!"
                },
            status_code=200    )