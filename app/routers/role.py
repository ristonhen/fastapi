from fastapi import FastAPI, Response,status,HTTPException, Depends, APIRouter
from .. import models, schemas ,utils,oauth2
from ..database import get_db
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

router = APIRouter(
    prefix="/role",
    tags=['Roles']
)
FORBIDDEN_KEYWORDS = ["drop", "delete", "update", "alter","insert","truncate",";"]

@router.get("/{id}")
def get_role(id: int ,db: Session = Depends(get_db),
                  current_user: int = Depends(oauth2.get_current_user)):
    
    roles = db.query(models.UspRole).filter(models.UspRole.id == str(id)).first()
    if not roles:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Role {id} not found')
    response_data = {"data": roles, "status": "success"}
    return response_data
@router.get("/")
def get_all_roles(db: Session = Depends(get_db),
                  current_user: int = Depends(oauth2.get_current_user)):
    
    roles = db.query(models.UspRole).all()
    if not roles:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Role {id} not found')
    response_data = {"data": roles, "status": True}
    return response_data

@router.post("/", status_code=status.HTTP_201_CREATED)
def add_role(role: schemas.RoleCreate, db: Session = Depends(get_db),
            current_user: int = Depends(oauth2.get_current_user)):
    existing_rold = db.query(models.UspRole).filter(models.UspRole.rolecode == role.rolecode).first()
    if existing_rold:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'Role name {role.rolecode} already exists.')

        
    role.created_by = current_user.username
    role.created_date = datetime.now()
    new_role = models.UspRole(**role.dict())
    print(new_role)
    db.add(new_role)
    db.commit()
    db.refresh(new_role)
    response_data = {"data": new_role, "status": "success"}
    return response_data

@router.put("/{id}")
def update_role(id: int, updated_role: schemas.RoleUpdate, db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):

    # Check if the user exists
    role = db.query(models.UspRole).filter(models.UspRole.id == str(id))

    existing_role = role.first()
    if not existing_role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Role {id} not found")

    #Check if the updated user object contains forbidden keywords in keys or values

    updated_role.modified_by= current_user.username
    updated_role.modified_date = datetime.now()
    role.update(updated_role.dict(),synchronize_session=False)
    db.commit()
    db.refresh(existing_role)
    response_data = {"data": existing_role, "status": "success"}
    return {"data":response_data, "status": True}

@router.delete("/")
def delete_roles(ids: schemas.RoleDelete, db: Session = Depends(get_db),
                    current_user: int = Depends(oauth2.get_current_user)):

    # Check if any of the branches exist
    existing_roles = db.query(models.UspRole).filter(models.UspRole.id.in_(ids.roleid)).all()
    if not existing_roles:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No role found")

    # Delete the branches from the database
    deleted_roles = []
    # not_found_roles = []
    all_ids_exist = True  # Flag to track if all IDs exist

    for roleid in ids.roleid:
        role = next((r for r in existing_roles if r.id == roleid), None)
        if role:
            db.delete(role)
            deleted_roles.append(roleid)
        else:
            # not_found_roles.append(roleid)
            all_ids_exist = False  # Set flag to False if any ID is not found

    if not all_ids_exist:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="One or more roles not found")

    db.commit()

    message = ""
    if deleted_roles:
        message += f"{len(deleted_roles)} roles deleted successfully. "
    # if not_found_roles:
    #     message += f"Roles not found: {not_found_roles}"

    return {"status":True,"message": message}