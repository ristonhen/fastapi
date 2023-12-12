from fastapi import Response,status,HTTPException, Depends, APIRouter,Request
from pydantic import BaseModel, create_model
from sqlalchemy.orm import Session
from .. import models, schemas ,oauth2
from ..database import get_db, Base
from typing import Optional,Dict,List,cast
from datetime import datetime

from ..schemas import generate_pydantic_model

router = APIRouter()

# endpoints = ["company", "branch", "role"]

def create_handler(model_class):
    class_name = model_class.__name__
    endpoint = class_name.lower()

    @router.get(f"/{endpoint}/{{id}}", tags=[class_name])
    def get_id_handler(id: int ,db: Session = Depends(get_db),    
                current_user: int = Depends(oauth2.get_current_user)):
        query = db.query(model_class).filter(model_class.id == str(id)).first()
        if not query:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'{model_class} {id} not found')
        response_data = {"data": query, "status": "success"}
        return response_data
    @router.get(f"/{endpoint}", tags=[class_name])
    async def get_handler( db: Session = Depends(get_db),
                    current_user: int = Depends(oauth2.get_current_user)):
        query = db.query(model_class).all()
        return {"data": query, "status": True}
    
    @router.post(f"/{endpoint}", tags=[class_name])
    async def post_handler(request_data: generate_pydantic_model(model_class), db: Session = Depends(get_db),
                        #    current_user: int = Depends(oauth2.get_current_user)
                           ):
        # request_data.created_by = current_user.username
        request_data.created_date = datetime.now()
        new_data = model_class(**request_data.dict(), )
        
        db.add(new_data)
        db.commit()
        db.refresh(new_data)
        respone_data = {"data": new_data, "status": True}
        return respone_data

    @router.delete(f"/{endpoint}", tags=[class_name])
    async def delete_handler(ids: schemas.HandlerDelete, db: Session = Depends(get_db),
                         current_user: int = Depends(oauth2.get_current_user)):
        existing = db.query(model_class).filter(model_class.id.in_(ids.ids)).all()

        if not existing:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"id request not found")
        
        # Delete the branches from the database
        deleted_roles = []
        # not_found_roles = []
        all_ids_exist = True  # Flag to track if all IDs exist

        for id in ids.ids:
            item = next((r for r in existing if r.id == id), None)
            if item:
                db.delete(item)
                deleted_roles.append(item)
            else:
                # not_found_roles.append(roleid)
                all_ids_exist = False  # Set flag to False if any ID is not found
        if not all_ids_exist:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="One or more item not found")
        
        db.commit()

        message = ""
        if deleted_roles:
            message += f"{len(deleted_roles)} roles deleted successfully."
        return {"message": message}
    return { get_handler, get_id_handler, post_handler,delete_handler}
    # return get_handler, post_handler, delete_handler,get_id_handler

# Exclude the Base class from iteration
for model_name, model_class in models.__dict__.items():
    if model_name != 'Base' and isinstance(model_class, type) and issubclass(model_class, models.Base):
        get_handler, post_handler,delete_handler,get_id_handler  = create_handler(model_class)
        
