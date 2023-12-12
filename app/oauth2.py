from jose import JWTError, jwt
from datetime import datetime , timedelta
from . import schemas,database,models
from fastapi import Depends, status ,HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import settings
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')
# SECRET_KEY
# Algorithm
# Expriration time
SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_access_token(data: dict):

    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({ "exp": expire })

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY,algorithm=ALGORITHM)

    return {"token":encoded_jwt, "expire":"123", "token_type": "bearer"}

def verify_access_token(token: str, credentails_exeption):

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("user_id")

        if id is None: 
            raise credentails_exeption
        token_data = schemas.TokenData(id=id)
    except JWTError as e:
        raise credentails_exeption
    
    except AssertionError as e:
        print(e)
    return token_data

async def get_current_user(token: str  = Depends(oauth2_scheme),db: Session = Depends(database.get_db)):
    credentails_exeption = HTTPException(status_code= status.HTTP_401_UNAUTHORIZED,
                                         detail=f"Could not validate credentials",
                                           headers={"WWW-Authenticate": "Bearer"})
    token = verify_access_token(token, credentails_exeption)

    user = db.query(
        models.User.id,
        models.User.username,
        models.User.fullname,
        models.User.email,
        models.User.password,
        models.User.last_pwd_modified_date,
        models.User.phone_number,
        models.User.branch_id,
        models.User.status,
        models.User.created_date,
        models.User.created_by,
        models.User.modified_date,
        models.User.modified_by,
        models.User.description,
        models.User.deviceid,
        models.UspRole.id.label('roleid'),
        models.UspRole.rolename,
        models.UspBranch.id.label('branch_id'),
        models.UspBranch.branch_name.label('branch_name'),
        models.Company.id.label('company_id'),
        models.Company.company_name
    ).join(models.UspBranch,models.User.branch_id == models.UspBranch.id
    ).join(models.Company, models.UspBranch.company_id == models.Company.id
    ).join(models.UspRole, models.User.roleid == models.UspRole.id
    ).filter(models.User.id == token.id).first()
    return user