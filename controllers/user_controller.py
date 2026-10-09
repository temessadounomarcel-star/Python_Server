from fastapi import  Request, Response, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from models import user
from Config.db import database, get_db


class UserController:
    def __init__(self):
        self.users = []

    #Création de l'utilisateur dans la base de données en utilisant le schéma UserSchema
    async def create_userSchema(self, req: Request, res: Response, db: Session = Depends(get_db)):
        data = await req.form()
        userName = data.get("username","").strip()
        email = data.get("email","").strip()
        password = data.get("password","").strip()
        id = len(self.users)
        
        if not userName or not email or not password:

            return JSONResponse(
                content={
                    "error": "Missing required fields"
                    }, 
                status_code=400
                )

        user_schema = user.UserSchema(username=userName, email=email, password=password)
        db.add(user_schema)
        db.commit()
        db.refresh(user_schema)
        return  JSONResponse(
            content={
            "message": "User created successfully"
            }, 
            status_code=201
            )


#Cette méthode récupère tous les utilisateurs dans la base de données
    async def get_users(self, req: Request, res: Response, db: Session = Depends(get_db)):
        #Récupération de tous les utilisateurs dans la base de données
        try:
            self.users = db.query(user.UserSchema).all()

            return JSONResponse(
                content=[user.to_dict() for user in self.users], 
                status_code=200
                )
        except Exception as e:
            print(f"Error occurred while fetching users: {e}")
            return JSONResponse(content={
                                        "error": "Failed to fetch users",
                                        "value": str(e)
                                        }, 
                                status_code=500)


#Cette méthode récupère un utilisateur par son ID dans la base de données
    async def get_user_by_id(self, req: Request, res: Response, db: Session = Depends(get_db)):
        id = int(req.query_params.get("id","Aucun ID fourni"))
        #Récupération de l'utilisateur par ID dans la base de données
        try:
            #Récupération de l'utilisateur par ID dans la base de données
            user_ = db.query(user.UserSchema).filter(user.UserSchema.id == id).first()

            return JSONResponse(content=user_.to_dict(), status_code=200) if user_  else JSONResponse(content={"error": "User not found"}, status_code=404)
        except Exception as e:
            print(f"Error occurred while fetching user by ID: {e}")
            return JSONResponse(content={
                                "error": "Failed to fetch user by ID"
                                }, 
                                status_code=500)

    def check_user_existence_by_id(self, user_id: int, db: Session) -> bool:
        user_ = db.query(user.UserSchema).filter(user.UserSchema.id == user_id).first()
        return user_ is not None
      





