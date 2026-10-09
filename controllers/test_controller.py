from fastapi import Depends, HTTPException, Request, Response
from sqlalchemy import text
from sqlalchemy.orm import Session



#test de la connexion

async def test_database_controller(req: Request, res: Response, db: Session ):
    try:
        result = db.execute(text("SELECT DATABASE()")).scalar_one()

        return {
            "message": "Connexion MySQL réussie",
            "database": result,
        }

    except Exception as exc:
        raise HTTPException(
            status_code=503,
            detail="Impossible de communiquer avec MySQL",
        ) from exc
