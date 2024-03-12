import os
import shutil
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from . import models
# from fastapi.app.routers.dynamicRouter import router
from .database import engine
from .routers import post, user,auth , vote, menu, index, branch,role,configuration,dynamicRouter, sentmail
from typing import List,Optional, Union
# from datetime import datetime
from . import schemas
from app.sockets import sio_app

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

app.include_router(dynamicRouter.router)
app.include_router(sentmail.router)
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)
app.include_router(menu.router)
app.include_router(index.router)
app.include_router(branch.router)
app.include_router(role.router)
app.include_router(configuration.router)
app.mount('/api', app=sio_app)

@app.get("/")
def read_root():
    return {'message': 'Hello👋 Developers💻'}


# class FindFile(BaseModel):
#     refid: List[str]
#     directory_path: str
#     target_folder_path: str

# @app.post("/findtxt")
# def findtext(request: FindFile):
#     max_file_size = 1000 
    
#     # directory_path = request.directory_path
#     directory_path = r"D:\DB Team\1ST-11.03.2024"
#     target_folder_path = f"{directory_path}/copy_new"
#     file_names = print_directory_contents(directory_path, target_folder_path, request.refid, max_file_size)
#     return {'message': 'Hello👋 Developers💻', 'file_names': file_names}

# def print_directory_contents(directory, target_folder, accountname, max_file_size):
#     file_names = []
#     for item in os.listdir(directory):

#         item_path = os.path.join(directory, item)
#         if os.path.isdir(item_path):
#             file_names.extend(print_directory_contents(item_path, target_folder, accountname, max_file_size))
#         else:
#             file_size = os.path.getsize(item_path)
#             if file_size < max_file_size:
#                 with open(item_path, 'r', encoding='utf-8', errors='ignore') as file:
#                     file_content = file.read()
#                     if any(name in file_content for name in accountname):
#                         # Create the target folder if it doesn't exist
#                         if not os.path.exists(target_folder):
#                             os.makedirs(target_folder)
                        
#                         # Copy the file to the target folder without changing its date
#                         target_path = os.path.join(target_folder, item)
#                         try:
#                             shutil.copy2(item_path, target_path)
#                             file_names.append(item)
#                         except PermissionError:
#                             # Handle the exception (e.g., log an error message or skip the file)
#                             pass
                    
#     return file_names




# {
#   "refid": [
#     "6624633067FS"
#   ],
#   "directory_path": "app/assets,1ST-11.03.2024",
#   "target_folder_path": "app/assets/1ST-11.03.2024"
# }




if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)