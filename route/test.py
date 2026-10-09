from fastapi import APIRouter, Request, Response
from sqlalchemy.orm import Session
from fastapi import Depends
from Config.db import get_db


from controllers.test_controller import test_database_controller as test



router = APIRouter()

@router.get("/")
async def test_database(req: Request, res: Response, db: Session = Depends(get_db)):
    return await test(req, res, db)