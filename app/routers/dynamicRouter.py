from fastapi import status, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from .. import models, schemas ,oauth2
from ..database import get_db
from typing import  List
from datetime import datetime
from ..schemas import generate_pydantic_model
import logging

logger = logging.getLogger(__name__)
router = APIRouter(
    prefix="/api"
)

def create_handler(model_class):
    class_name = model_class.__name__
    endpoint = class_name.lower()

    @router.get(f"/{endpoint}/{{id}}", tags=[class_name])
    def get_id_handler(id: int ,db: Session = Depends(get_db),    
                current_user: int = Depends(oauth2.get_current_user)):
        query = db.query(model_class).filter(model_class.id == str(id)).first()
        if not query:
            response_data = schemas.Response(
                status=status.HTTP_200_OK,
                message=f"No records found",
                data={endpoint: []}
            )
            return response_data

        # Get the column names dynamically from the model's table
        columns = model_class.__table__.columns.keys()
        result_data = {column: getattr(query, column) for column in columns}
        response_data = schemas.Response(
            status=status.HTTP_200_OK,
            message=f"1 Record query successfully",
            data={endpoint: result_data}
        )
        return response_data
    
    @router.get(f"/{endpoint}", tags=[class_name])
    async def get_handler( db: Session = Depends(get_db),
                    current_user: int = Depends(oauth2.get_current_user)):
        query = db.query(model_class).all()
        if not query:
            response_data = schemas.Response(
                status=status.HTTP_200_OK,
                message=f"No records found",
                data={endpoint: []}
            )
            return response_data
        # Get the column names dynamically from the model's table
        columns = model_class.__table__.columns.keys()
        # Create dictionaries with desired attributes dynamically
        json_data = [
            {column: getattr(data, column) for column in columns}
            for data in query
        ]
        response_data = schemas.Response(
            status=status.HTTP_200_OK,
            message=f"{len(json_data)} Record query successfully",
            data={endpoint: json_data}
        )
        return response_data

    @router.post(f"/{endpoint}", tags=[class_name], response_model=schemas.Response)
    async def post_handler(request_data: List[generate_pydantic_model(model_class)], db: Session = Depends(get_db), # type: ignore
                           current_user: int = Depends(oauth2.get_current_user)):
        response_data_list = []  # List to collect individual responses
        error_list = []  # List to collect individual errors
        try:
            for index, data in enumerate(request_data, start=1):  # Use enumerate to get the index
                data.created_by = current_user.username
                data.created_date = datetime.now()
                data = model_class(**data.dict())
                db.add(data)
                db.commit()
                db.refresh(data)
                
                # Convert the Base object to a dictionary
                # columns = model_class.__table__.columns.keys()
                new_data_dict = {column: getattr(data, column) for column in data.__table__.columns.keys()}
                response_data_list.append(new_data_dict)  
                              
                
            response_data = schemas.Response(
                status=status.HTTP_200_OK,
                message=f"{len(response_data_list)} Record created successfully",
                data={endpoint: response_data_list}
            )
        except IntegrityError as e:
            db.rollback()
            error_message = str(e.orig)
            logger.error(f"IntegrityError while creating records: {error_message}")

            if "unique constraint" in error_message.lower():
                duplicate_value = error_message.split("Key (")[1].split(")=")[0]
                error_list.append({"message": f"Duplicate entry for {duplicate_value}"})
            else:
                error_list.append({"message": error_message})
            response_data = schemas.Response(
                status=status.HTTP_400_BAD_REQUEST,
                message=f"one or more records insert with errors",
                data={"errors": error_list}
            )
        except Exception as e:
            db.rollback()      
            error_message = str(e)
            logger.error(f"Error while creating records: {error_message}")
            response_data = schemas.Response(
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                message="Internal server Maintenance",
                data={"errors": [{"message": error_message}]}
            )
        return response_data

    @router.put(f"/{endpoint}/{{id}}", tags=[class_name])
    async def update_handler(id: int, request_data: generate_pydantic_model(model_class, for_insert=False, skip_fields=["created_by", "created_date"]), # type: ignore
                        db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):        
        existing_data = db.query(model_class).filter(model_class.id == id).first()
        if not existing_data:
            response_data = schemas.Response(
                status=status.HTTP_200_OK,
                message=f'old_account with the id {id} is not available',
                data={endpoint: {}}
            )
            return response_data
        # Update all fields with the new data
        request_data.modified_by = current_user.username
        request_data.modified_date = datetime.now()
        
        for field, value in request_data.dict(exclude_unset=True).items():
            setattr(existing_data, field, value)
        db.commit()
        db.refresh(existing_data)
        
        # Query the database again to get the updated data
        updated_data = db.query(model_class).filter(model_class.id == id).first()
        columns = model_class.__table__.columns.keys()
        result_data = {column: getattr(updated_data, column) for column in columns}

        response_data = schemas.Response(
            status=status.HTTP_200_OK,
            message=f"1 Record Updated successfully",
            data={endpoint: result_data}
        )
        return response_data
    
    @router.delete(f"/{endpoint}", tags=[class_name])
    async def delete_handler(ids: schemas.HandlerDelete, db: Session = Depends(get_db),
                         current_user: int = Depends(oauth2.get_current_user)):
        existing = db.query(model_class).filter(model_class.id.in_(ids.ids)).all()

        if not existing:
            return {"status": status.HTTP_404_NOT_FOUND, "message":"Request id not found"}
        
        # Delete the branches from the database
        deleted_items = []
        # not_found_roles = []
        all_ids_exist = True  # Flag to track if all IDs exist

        for id in ids.ids:
            item = next((r for r in existing if r.id == id), None)
            if item:
                db.delete(item)
                deleted_items.append(item)
            else:
                # not_found_roles.append(roleid)
                all_ids_exist = False  # Set flag to False if any ID is not found
        if not all_ids_exist:
            db.rollback()
            return {"status":status.HTTP_404_NOT_FOUND, "message":"One or more item not found"}
        
        db.commit()

        message = ""
        if deleted_items:
            message += f"{len(deleted_items)} Item deleted successfully."
        
        response_data = schemas.Response(
            status=status.HTTP_200_OK,
            message=message,
            data={endpoint: {}}
        )
        return response_data
    return { get_handler, get_id_handler, post_handler, update_handler, delete_handler}

# Exclude the Base class from iteration
for model_name, model_class in models.__dict__.items():
    if model_name != 'Base' and isinstance(model_class, type) and issubclass(model_class, models.Base):
        get_id_handler, get_handler, post_handler,update_handler, delete_handler = create_handler(model_class)
        
