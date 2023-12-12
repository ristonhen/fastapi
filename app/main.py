from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from . import models ,schemas
from app.routers.router import router
from .database import engine
from .routers import post, user,auth , vote, menu, index, branch,role,configuration
from pydantic import BaseModel, create_model
from typing import List,Optional, Union
from datetime import datetime
# from .schemas import create_dynamic_model


#  auto generate table to DB
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    # # How to Disable the Docs (Swagger UI and ReDoc)
    # docs_url=None, # Disable docs (Swagger UI)
    # redoc_url=None, # Disable redoc
)
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(router, prefix="/api")
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)
app.include_router(menu.router)
app.include_router(index.router)
app.include_router(branch.router)
app.include_router(role.router)
app.include_router(configuration.router)


# Test dynamic create field
def create_dynamic_model(fields: List[Union[str, dict]]) -> BaseModel:
    field_definitions = {}
    for field in fields:
        if isinstance(field, str):
            field_definitions[field] = (str, ...)
        elif isinstance(field, dict):
            field_name = field['name']
            field_type = field['type']
            field_definitions[field_name] = (field_type, ...)
    
    DynamicModel = create_model('DynamicModel', **field_definitions)
    return DynamicModel

@app.get("/")
def read_root():
    dynamic_fields = [
        'name',
        'age',
        {'name': 'birth_date', 'type': Optional[datetime]}
    ]
    DynamicModel = create_dynamic_model(dynamic_fields)
    data = {
        'name': 'Alice',
        'age': 25,
        'birth_date': datetime.now()  # Assign a datetime value
    }
    dynamic_instance = DynamicModel(**data)
    # Access the dynamically generated fields
    return dynamic_instance


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)