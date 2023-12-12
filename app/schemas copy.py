from pydantic import BaseModel,EmailStr,create_model
from datetime import datetime
from typing import Optional,Dict,List,Union
from pydantic.types import conint

field_definitions = {
    'user_id': Optional[int],
    'fullname': Optional[str],
    'email': Optional[EmailStr],
    'branch_id': Optional[int],
    'roleid': Optional[int],
    'phone_number': Optional[int],
    'created_by': Optional[str],
    'created_date': Optional[datetime],
    'modified_by': Optional[str],
    'modified_date': Optional[datetime],
    'last_pwd_modified_date': Optional[datetime],
    'description': Optional[str],
    'deviceid': Optional[str]
}

model_definitions = [
    {
        'model_name': 'DynamicUser',
        'fields': {
            'user_id': (Optional[int], ...),
            'fullname': (Optional[str], ...),
            'email': (Optional[str], ...),
            'branch_id': (Optional[int], ...),
            'roleid': (Optional[int], ...),
            'phone_number': (Optional[int], ...),
            'created_by': (Optional[str], ...),
            'created_date': (Optional[datetime], ...),
            'modified_by': (Optional[str], ...),
            'modified_date': (Optional[datetime], ...),
            'last_pwd_modified_date': (Optional[datetime], ...),
            'description': (Optional[str], ...),
            'deviceid': (Optional[str], ...),
        }
    },
    {
        'model_name': 'DynamicProduct',
        'fields': {
            'product_id': (Optional[int], ...),
            'name': (Optional[str], ...),
            'price': (Optional[float], ...),
            # ... other fields
        }
    },
    # ... add more models as needed
]

dynamic_models = {}
for model_definition in model_definitions:
    model_name = model_definition['model_name']
    fields = model_definition['fields']
    dynamic_models[model_name] = create_model(model_name, **fields)

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class UserBase(BaseModel):
    user_id: Optional[int]
    fullname: Optional[str]
    email: Optional[EmailStr]
    branch_id: Optional[int]
    roleid: Optional[int]
    phone_number: Optional[int]
    created_by: Optional[str]
    created_date: Optional[datetime]
    modified_by: Optional[str]
    modified_date: Optional[datetime]
    last_pwd_modified_date:Optional[datetime]
    description: Optional[str]
    deviceid: Optional[str]
    

    class Config:
        orm_mode = True
# class UserOut(UserBase):
#     branch_name: Optional[str]
#     rolename: Optional[str]
class UserOut(dynamic_models['DynamicUser']):
    branch_name: Optional[str]
    rolename: Optional[str]

class UserListResponse(BaseModel):
    users: List[UserOut]
    status: bool = True

class PostCreate(PostBase):
    pass

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
class UserCreate(BaseModel):
    fullname: str
    email: EmailStr
    password: str
    branch_id: int
    roleid: int
    created_by: Optional[str] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token (BaseModel):
    user: UserBase
    access_token: Dict[str, str]
    # token_type: str

    class Config:
        orm_mode = True

class TokenData(BaseModel):
    id: Optional[str] = None
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
    pmsid: Optional[int]
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


