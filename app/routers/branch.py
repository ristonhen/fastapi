from fastapi import FastAPI, Response,status,HTTPException, Depends, APIRouter
from .. import models, schemas ,utils,oauth2
from ..database import get_db
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

router = APIRouter(
    prefix="/branch",
    tags=['Branches']
)
@router.post("/", status_code=status.HTTP_201_CREATED)
def add_branch(branch: schemas.BranchCreate, db: Session = Depends(get_db),
             current_user: int = Depends(oauth2.get_current_user)):
    branch.created_by = current_user.username
    branch.created_date = datetime.now()
    new_brach = models.UspBranch(**branch.dict())
    db.add(new_brach)
    db.commit()
    db.refresh(new_brach)
    
    return {"data":new_brach, "status": True}

@router.get("/{id}")
def get_branch(id: int ,db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    branch = db.query(models.UspBranch).filter(
        models.UspBranch.id == str(id)).first()
    if not branch:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Branch {id} not found")
    return branch

@router.get("/")
def get_all_branches(db: Session = Depends(get_db),
                  current_user: int = Depends(oauth2.get_current_user)):
    
    branches = db.query(models.UspBranch).all()
    if not branches:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Branch {id} not found")
    return {"data":branches, "status": True}

@router.put("/{id}")
def update_branch(id: int, updated_branch: schemas.BranchUpdate, db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):

    # Check if the user exists
    user = db.query(models.UspBranch).filter(models.UspBranch.id == str(id))

    existing_user = user.first()
    if not existing_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User {id} not found")

    #Check if the updated user object contains forbidden keywords in keys or values

    updated_branch.modified_by= current_user.username
    updated_branch.modified_date = datetime.now()
    user.update(updated_branch.dict(),synchronize_session=False)
    db.commit()
    db.refresh(existing_user)

    return {"data":existing_user, "status": True}

@router.delete("/")
def delete_branches(ids: schemas.HandlerDelete, db: Session = Depends(get_db),
                    current_user: int = Depends(oauth2.get_current_user)):

    # Check if any of the branches exist
    existing_branch = db.query(models.UspBranch).filter(models.UspBranch.id.in_(ids.ids)).all()
    if not existing_branch:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No role found")

    # Delete the branches from the database
    deleted_branch = []
    # not_found_branch = []
    all_ids_exist = True  # Flag to track if all IDs exist

    for branchId in ids.ids:
        role = next((r for r in existing_branch if r.id == branchId), None)
        if role:
            db.delete(role)
            deleted_branch.append(branchId)
        else:
            # not_found_branch.append(branchId)
            all_ids_exist = False  # Set flag to False if any ID is not found

    if not all_ids_exist:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="One or more branch not found")

    db.commit()

    message = ""
    if deleted_branch:
        message += f"{len(deleted_branch)} branch deleted successfully. "
    # if not_found_branch:
    #     message += f"branch not found: {not_found_branch}"

    return {"status":True,"message": message}