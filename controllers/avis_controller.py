from models.avis import Avis
from fastapi import Request, Response, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
import controllers.user_controller as user_controller  

class AvisController:
    def __init__(self):
        self.avis=[]
        self.user = user_controller.UserController()

    async def create_avis(self, req: Request, res: Response, db: Session):
        try:
            data = await req.form()
            user_id = int(data.get("user_id").strip())
            message = str(data.get("avis")).strip()
            if not self.user.check_user_existence_by_id(user_id, db):
                return JSONResponse(status_code=404, content={"message": "Utilisateur non trouvé"})

            avis_ = Avis(user_id=user_id, avis=message)
            db.add(avis_)
            db.commit()
            db.refresh(avis_)
            return JSONResponse(status_code=201, content={"message": "Avis créé avec succès", "avis": avis_.to_dict()})
        except Exception as e:
            return JSONResponse(status_code=400, content={"message": "Erreur lors de la création de l'avis"+ str(e)})
       