from fastapi import status,HTTPException, Depends, APIRouter
from .. import models, schemas ,utils,oauth2
from ..database import get_db
from sqlalchemy.orm import Session
from datetime import datetime

router = APIRouter(
    prefix="/configuration",
    tags=['Configuration']
)
@router.get("/{id}")
def get_config(id: int ,db: Session = Depends(get_db),
                  current_user: int = Depends(oauth2.get_current_user)):
    config = db.query(models.UspConfiguration).filter(models.UspConfiguration.id == str(id)).first()
    if not config:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Config {id} not found')
    response_data = {"data": config, "status": "success"}
    return response_data

@router.get("/")
def get_all_config(db: Session = Depends(get_db),
                  current_user: int = Depends(oauth2.get_current_user)):
    configs = db.query(models.UspConfiguration).all()
    if not configs:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Config {id} not found')
    response_data = {"data": configs, "status": True}
    return response_data

@router.post("/", status_code=status.HTTP_201_CREATED)
def add_config(config: schemas.ConfigCreate, db: Session = Depends(get_db),
            current_user: int = Depends(oauth2.get_current_user)):
    existing_rold = db.query(models.UspConfiguration).filter(models.UspConfiguration.paramname == config.paramname).first()
    if existing_rold:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'Config name {config.paramname} already exists.')
    config.created_by = current_user.username
    config.created_date = datetime.now()
    new_config = models.UspConfiguration(**config.dict())
    db.add(new_config)
    db.commit()
    db.refresh(new_config)
    response_data = {"data": new_config, "status": "success"}
    return response_data

@router.put("/{id}")
def update_config(id: int, updated_config: schemas.ConfigUpdate, db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):

    # Check if the user exists
    config = db.query(models.UspConfiguration).filter(models.UspConfiguration.id == str(id))
    existing_config = config.first()
    if not existing_config:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Configuration {id} not found")
    #Check if the updated user object contains forbidden keywords in keys or values
    updated_config.modified_by= current_user.username
    updated_config.modified_date = datetime.now()
    config.update(updated_config.dict(),synchronize_session=False)
    db.commit()
    db.refresh(existing_config)
    response_data = {"data": existing_config, "status": "success"}
    return response_data

@router.delete("/")
def delete_config(ids: schemas.HandlerDelete, db: Session = Depends(get_db),
                    current_user: int = Depends(oauth2.get_current_user)):
    # Check if any of the branches exist
    existing_config = db.query(models.UspConfiguration).filter(models.UspConfiguration.id.in_(ids.ids)).all()
    if not existing_config:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No configuration found")

    deleted_config = []
    all_ids_exist = True  # Flag to track if all IDs exist
    for config_id in ids.ids:
        Config = next((r for r in existing_config if r.id == config_id), None)
        if Config:
            db.delete(Config)
            deleted_config.append(config_id)
        else:
            all_ids_exist = False  # Set flag to False if any ID is not found

    if not all_ids_exist:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="One or more Configs not found")

    db.commit()

    message = ""
    if deleted_config:
        message += f"{len(deleted_config)} Configs deleted successfully."

    return {"messsage": message,"status":True}