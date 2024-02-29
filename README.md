# fastapi
## Create an environment
Create a project folder and a .venv folder within:
```sh
py -3 -m venv venv

```
## Activate the environment
Before you work on your project, activate the corresponding environment:
```sh
.venv\Scripts\activate
```
## install FastAPI
```sh
pip install fastapi[all]
```
## Install the Server Program
```sh
pip install "uvicorn[standard]"

```
## Install psycopg2
```sh
pip install psycopg2

```

## Install SQLAlchemy
```sh
pip install SQLAlchemy

```
## Install pydantic-settings
```sh
pip install pydantic-settings

```

## Install EmailStr
```sh
pip install email-validator

```
## Install alembic
```sh
pip install alembic
```
## OAuth2 with Password (and hashing), Bearer with JWT tokens
Install python-jose
```sh
pip install "python-jose[cryptography]"
```
## Password hashing
```sh
pip install "passlib[bcrypt]"
```
## Install  PyCryptodome
```sh
pip install pycryptodome
```
## Install  python-multipart
```sh
pip install python-multipart
```
## For Sent Mail outlook
```sh
pip install python-socketio
```
## For Sent Mail outlook
```sh
--------------
```



## After clone project 
``` sh 
python3 -m venv venv
pip install -r requirements.txt
pip freeze                                ## To show all
pip freeze > requirements.txt             ## To generate from env lib(all lib we installed)
```
## run App
```sh
#uvicorn main:app                          
#uvicorn app.main:app --reload
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```


route param
posts?limit=10&skip=2&search=to

https://youtu.be/0sOvCWFmrtA?t=39918


…or create a new repository on the command line
echo "# fastapi" >> README.md
  git init
  git add README.md
  git commit -m "first commit"
  git branch -M main
  git remote add origin https://github.com/ristonhen/fastapi.git
  git push -u origin main
…or push an existing repository from the command line
git remote add origin https://github.com/ristonhen/fastapi.git
  git branch -M main
  git push -u origin main


  ## Schema version code V2
```sh
from pydantic import BaseModel,EmailStr,create_model,Field
from sqlalchemy.ext.declarative import DeclarativeMeta

from datetime import datetime
from typing import Optional,Dict,List, Any,Type
from pydantic.types import conint
from . import models

# Generate Pydantic model dynamically based on the SQLAlchemy model
def generate_pydantic_model(sa_model: DeclarativeMeta) -> Type[BaseModel]:
    fields = {}
    for column in sa_model.__table__.columns:
        if column.primary_key:
            continue  # Skip the 'id' column
        field_type = column.type.python_type
        field_name = column.name
        is_required = not column.nullable and column.default is None

        if is_required:
            fields[field_name] = (field_type, ...)
        elif not is_required:
            fields[field_name] = (Optional[field_type], ...)
        else:
            fields[field_name] = (Optional[field_type], None)  # assuming all other fields are optional
        fields[field_name] = (Optional[field_type], None)  # assuming all fields are optional
    # pydantic_model = type(sa_model.__name__, (BaseModel,), fields)
    pydantic_model = create_model(sa_model.__name__ + "Model", **fields)
    return pydantic_model
```