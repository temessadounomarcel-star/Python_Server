
from fastapi import APIRouter, Request, Response
from config import settings
from controllers import home_controller
router = APIRouter()

controller = home_controller.HomeController()

@router.get("/")
async def accueil(req : Request, res : Response):
    return await controller.accueil(req, res)

@router.post("/")
async def test(req : Request, res : Response):
    return await controller.post_message(req, res)

@router.delete("/")
async def delete(req : Request, res : Response):
    return await controller.delete_message(req, res)
    