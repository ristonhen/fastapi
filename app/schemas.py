from pydantic import BaseModel,EmailStr,create_model,Field
from datetime import datetime
from typing import Optional,Dict,List
from pydantic.types import conint
from . import models

# Generate Pydantic model dynamically based on the SQLAlchemy model
def generate_pydantic_model(sa_model):
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

class SentEmailReviewAml(BaseModel):
    branchname: str
    email_to: List[str]
    cc_email: List[str]
    pdfimage: str
    
class SentEmailReviewAmlList(BaseModel):
    email_data: List[SentEmailReviewAml]
class DatabaseInfo(BaseModel):
    database_backend: str

class HandlerDelete(BaseModel):
    ids: List[int]

class RoleBase(BaseModel):
    # roleid: int
    rolecode:str
    rolename: str

class RoleCreate(RoleBase):
    created_date: Optional[datetime]
    created_by: Optional[str]
class RoleUpdate(RoleBase):
    modified_date:Optional[str]
    modified_by:Optional[str]

class RoleDelete(BaseModel):
    roleid: List[int]

class RoleOut(RoleBase):
    id: int
    created_date: datetime
    created_by: str
    created_date: datetime
    created_by: str

class BranchBase(BaseModel):
    branch_code: str
    branch_name: str
    range_ip: Optional[int]
    tvticketip: Optional[str]
    company_id: int

class BranchCreate(BranchBase):
    opening_date: Optional[str] =None
    created_date: Optional[datetime] = None
    created_by: Optional[str] = None

class BranchUpdate(BranchBase):
    modified_date: Optional[datetime] 
    modified_by: Optional[str]

class BranchDelete(BaseModel):
    id: List[int]
    opening_date: Optional[str]
    created_date: Optional[datetime]
    created_by: Optional[str] = None
    modified_date: Optional[datetime] 
    modified_by: Optional[str]

class BranchOut(BranchBase):
    branch_id: int


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class UserBase(BaseModel):
    id: int
    username: str
    fullname: str
    email: EmailStr
    branch_id: int
    roleid: Optional[int]
    phone_number: Optional[int]
    created_by: str
    created_date: datetime
    modified_by: Optional[str]
    modified_date: Optional[datetime]
    last_pwd_modified_date:Optional[datetime]
    description: Optional[str]
    deviceid: Optional[str]
    branch_name: Optional[str]
    rolename: Optional[str]
    company_name: Optional[str]
    class Config:
        orm_mode = True
class UserOut(BaseModel):
    user: UserBase
    status: Optional[bool] = True

class UserListResponse(BaseModel):
    users: List[UserBase]
    status: bool = True

class UserCreate(BaseModel):
    fullname: str
    username: str
    email: EmailStr
    password: Optional[str] =None
    branch_id: int
    roleid: int
    created_by: Optional[str] = None
    created_date: Optional[datetime] = None

class UserUpdate(BaseModel):
    fullname: str
    username: str
    email: EmailStr
    branch_id: int
    roleid: int
    phone_number: Optional[int] = None
    modified_by: Optional[str]
    modified_date: Optional[datetime]

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class ChangePasswordRequest(BaseModel):
    username: str
    currentassword: str
    newpassword: str
    lastpasswordmodifieddate: Optional[datetime]

class ResetPasswordRequest(BaseModel):
    email: str

class VerifyResetTokenRequest(BaseModel):
    email: str
    token: str
    newpassword: str

class VerifyResetTokenRequestByLink(BaseModel):
    token: str
    password: str


class Token (BaseModel):
    user: UserBase
    access_token: Dict[str, str]

    class Config:
        orm_mode = True

class TokenData(BaseModel):
    id: Optional[str] = None
    
class PostCreate(PostBase):
    pass

class ConfigCreate(BaseModel):
    paramname: str
    value: str
    created_by: Optional[str] = None
    created_date: Optional[datetime] =None

class ConfigUpdate(BaseModel):
    paramname: str
    value: str
    modified_by: Optional[str] = None
    modified_date: Optional[datetime] =None




class Post(PostBase):
    id: int
    create_date: datetime
    owner_id: int
    owner: UserBase
    class Config:
        orm_mode = True

class PostOut(BaseModel):
    Post: Post
    votes: int

    class Config:
        orm_mode = True

class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)

# User 

class MenuBase(BaseModel):
    # pmsid: Optional[int]
    pms_menu_name: str
    pms_menu_level: int
    pms_parent_id: Optional[int]
    to_name: str
    pms_menu_type: str
    pms_menu_index: int
    pms_menu_image: str
    created_date: Optional[datetime]
    created_by: Optional[str]
    modified_date:Optional[datetime]
    modified_by: Optional[str]
    db_id: Optional[int]
class MenuCreate(MenuBase):
    pass

class Menu(MenuBase):
    pass
# Menu
class MenuAssignedRoleOut(BaseModel):
    id: Optional[int]
    pms_menu_name: str
    pms_menu_level: int
    pms_parent_id: Optional[int]
    to_name: str
    pms_menu_type: str
    pms_menu_index: int
    pms_menu_image: str
    created_date: datetime
    created_by: str
    modified_date:Optional[datetime]
    modified_by: Optional[str]
    db_id: Optional[int]
    # pms_parent_name: int = "1"

