from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from .. import models, schemas ,oauth2
from ..database import default_database_backend

router = APIRouter(
    prefix="/switch-database-backend",
    tags=['switch-database-backend']
)
@router.post("/")
def switch_database(database_info: schemas.DatabaseInfo):
    database_backend = database_info.database_backend

    if database_backend:
        default_database_backend(database_backend)
        return {"message": f"Switched to {database_backend} backend."}
    else:
        raise HTTPException(status_code=400, detail="Invalid request. Missing 'database_backend' field.")