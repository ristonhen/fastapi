from fastapi import FastAPI, Response,status,HTTPException, Depends, APIRouter
from .. import models, schemas ,utils,oauth2
from ..database import get_db
from sqlalchemy.orm import Session
from typing import List
from app.models import UspRole
from datetime import datetime

router = APIRouter(
    prefix="/users",
    tags=['Users']
)
FORBIDDEN_KEYWORDS = ["drop", "delete", "update", "alter","insert","truncate",";"]
@router.post("/", status_code=status.HTTP_201_CREATED)
def add_user(user: schemas.UserCreate, db: Session = Depends(get_db),
             current_user: int = Depends(oauth2.get_current_user)):
    # Check if the user already exists
    existing_user = db.query(models.User).filter(
        models.User.email == user.email).first()
    existing_username = db.query(models.User).filter(
        models.User.username == user.username).first()

    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")
    if existing_username:
        raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST, detail="User Name already exists")
    # get default password
    defaultPasswordRow = db.query(models.UspConfiguration.value).filter(models.UspConfiguration.id == 1).first()
    # Create a new User object with the provided data

    # hash_password = utils.hash(user.password)            # for client request
    user.password = utils.hash(defaultPasswordRow.value)   # for default password
    # user.password = hash_password
    user.created_by = current_user.username
    new_user = models.User(**user.dict())
    db.add(new_user)                                       # Add the new user to the database
    db.commit()
    db.refresh(new_user)
    return {"data": new_user, "status":True}

@router.get("/{id}")
def get_user(id: int ,db: Session = Depends(get_db),
                  current_user: int = Depends(oauth2.get_current_user)):
    
    user = db.query(models.User).filter(models.User.id == str(id)).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Role {id} not found')
    return {"data": user, "status": "success"}

@router.get("/", response_model=schemas.UserListResponse)
def get_all_users(db: Session = Depends(get_db),
                  current_user: int = Depends(oauth2.get_current_user)):

    # company_filter =  models.UspRole.id == current_user.roleid
    # if(current_user.roleid == "MAIN"):
    #     company_filter = models.Company.id > 0
    query = db.query(
        models.User,
        models.UspBranch.branch_name,
        models.UspRole.rolename,
        models.Company.company_name
    ).join(
        models.UspBranch,
        models.User.branch_id == models.UspBranch.id
    ).join(
        models.UspRole,
        models.User.roleid == models.UspRole.id
    ).join(
        models.Company,
        models.UspBranch.company_id == models.Company.id
    # ).filter(
    #     company_filter
    ).order_by(
        models.User.id
    )  
    result = query.all()
    users = []
    for item in result:
        user_data = {
            "id": item.User.id,
            "username": item.User.username,
            "fullname": item.User.fullname,
            "email": item.User.email,
            "branch_id": item.User.branch_id,
            "roleid": item.User.roleid,
            "phone_number": item.User.phone_number,
            "created_by": item.User.created_by,
            "created_date": item.User.created_date,
            "modified_by": item.User.modified_by,
            "modified_date": item.User.modified_date,
            "last_pwd_modified_date": item.User.last_pwd_modified_date,
            "description": item.User.description,
            "deviceid": item.User.deviceid,
            "branch_name": item.branch_name,
            "rolename": item.rolename,
            "company_name":item.company_name
        }
        users.append(user_data)
    if not users:
        raise HTTPException(status_code=404, detail="No users found")

    return schemas.UserListResponse(users=users)


@router.put("/{id}")
def update_user(id: int, updated_user: schemas.UserUpdate, db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):

    # Check if the user exists
    user = db.query(models.User).filter(models.User.id == str(id))
    existing_user = user.first()
    if not existing_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User {id} not found")
    
    #2 way to update
    # on modified_by get from current user login and modified date get form currnent_time_stamp
    updated_user.modified_by= current_user.username
    updated_user.modified_date = datetime.now()
    # 1 way
    ## Update the user object with the provided data
    # for field, value in updated_user.dict().items():
    #     setattr(existing_user, field, value)

    #2 way
    
    user.update(updated_user.dict(),synchronize_session=False)
    # Commit the changes to the database
    db.commit()
    db.refresh(existing_user)
    respone_data = user.first()
    return {"data": respone_data, "status": True}

@router.delete("/")
def delete_user(ids: schemas.HandlerDelete, db: Session = Depends(get_db),
                    current_user: int = Depends(oauth2.get_current_user)):

    # Check if any of the branches exist
    existing_users = db.query(models.User).filter(models.User.id.in_(ids.ids)).all()
    if not existing_users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No user found")

    # Delete the branches from the database
    deleted_users = []
    # not_found_roles = []
    all_ids_exist = True  # Flag to track if all IDs exist

    for userid in ids.ids:
        user = next((r for r in existing_users if r.id == userid), None)
        print(user)
        if user:
            db.delete(user)
            deleted_users.append(userid)
        else:
            # not_found_roles.append(roleid)
            all_ids_exist = False  # Set flag to False if any ID is not found

    if not all_ids_exist:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="One or more roles not found")

    db.commit()

    message = ""
    if deleted_users:
        message += f"{len(deleted_users)} roles deleted successfully. "
    # if not_found_roles:
    #     message += f"Roles not found: {not_found_roles}"

    return {"status":True,"message": message}
