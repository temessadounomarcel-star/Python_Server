from fastapi import APIRouter, Request, Response
from sqlalchemy.orm import Session
from fastapi import Depends
from Config.db import get_db
from controllers import user_controller
from controllers import avis_controller


router = APIRouter()
controller = user_controller.UserController()
avis_controller = avis_controller.AvisController()


@router.post("/create")
async def create_userSchema(req: Request, res: Response, db: Session = Depends(get_db)):
    return await controller.create_userSchema(req, res, db)

@router.get("/users")
async def get_user_by_id(req: Request, res: Response, db: Session = Depends(get_db)):
    return await controller.get_user_by_id(req, res, db)

@router.get("/")
async def get_users(req: Request, res: Response, db: Session = Depends(get_db)):
    return await controller.get_users(req, res, db)


#route pour ecrire les avis des utilisateurs
@router.post("/avis")
async def create_avis(req: Request, res: Response, db: Session = Depends(get_db)):
    return await avis_controller.create_avis(req, res, db)