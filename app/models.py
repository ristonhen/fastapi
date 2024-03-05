from .database import Base
from sqlalchemy import Column, Integer,String, Boolean, ForeignKey, Date, Text,UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.dialects.postgresql import JSONB
from typing import List, Optional
from pydantic import BaseModel, Field

class Company(Base):
    __tablename__ = 'companys'

    id = Column(Integer, primary_key=True, autoincrement=True,nullable= False)
    company_name = Column(String, nullable=False, unique=True)
    company_code = Column(String, nullable=False)
    created_date = Column(TIMESTAMP(timezone=True), nullable=False, server_default= text('now()'))
    created_by = Column(String, nullable=False)
    modified_date = Column(TIMESTAMP(timezone=True))
    modified_by = Column(String)
    opening_date = Column(TIMESTAMP(timezone=True), nullable=False)

class UspBranch(Base):
    __tablename__ = 'usp_branchs'

    id = Column(Integer, primary_key=True, autoincrement=True,nullable= False)
    branch_code = Column(String, nullable=False)
    branch_name = Column(String, nullable=False, unique=True)
    opening_date = Column(Date)
    range_ip = Column(Integer, nullable=False)
    created_date = Column(TIMESTAMP(timezone=True), nullable=False, server_default= text('now()'))
    created_by = Column(String, nullable=False)
    modified_date = Column(TIMESTAMP(timezone=True))
    modified_by = Column(String)
    tvticketip = Column(JSONB)
    company_id = Column(Integer, ForeignKey("companys.id",ondelete="CASCADE",onupdate="CASCADE"),nullable=False,)

class UspConfiguration(Base):
    __tablename__ = 'usp_configuration'
    id = Column(Integer, primary_key=True, autoincrement=True)
    paramname = Column(String, nullable=False, unique=True)
    value = Column(String)
    created_date = Column(TIMESTAMP(timezone=False), nullable=False,server_default= text('now()'))
    created_by = Column(String)
    modified_date = Column(TIMESTAMP(timezone=False))
    modified_by = Column(String)

    __table_args__ = (
        UniqueConstraint('paramname', name='usp_configuration_paramname_key'),
    )

class UspRole(Base):
    __tablename__ = 'usp_role'

    id = Column(Integer, primary_key=True,nullable=False, autoincrement=True)
    rolecode = Column(String, nullable=False, unique=True)
    rolename = Column(String, nullable=False, unique=True)
    created_date = Column(TIMESTAMP(timezone=True), nullable=False, server_default= text('now()'))
    created_by = Column(String)
    modified_date = Column(TIMESTAMP(timezone=True))
    modified_by = Column(String)

    __table_args__ = (
        UniqueConstraint('rolecode', name='usp_role_rolecode_key'),
        UniqueConstraint('rolename', name='usp_role_rolename_key')
    )

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer,primary_key=True, nullable= False, autoincrement=True)
    fullname = Column(String, nullable=False)
    username = Column(String,nullable=False, unique=True)
    email = Column(String , nullable=False , unique=True)
    password = Column(String, nullable=False)
    last_pwd_modified_date = Column(TIMESTAMP(timezone=True))
    phone_number = Column(String)
    branch_id = Column(Integer, ForeignKey("usp_branchs.id",ondelete="CASCADE",onupdate="CASCADE"),nullable=False,)
    status = Column(Boolean, nullable=False, server_default= text('true'))
    roleid = Column(Integer, ForeignKey('usp_role.id'), nullable=False)
    counterno = Column(String)
    created_date = Column(TIMESTAMP(timezone=True),nullable=False, server_default= text('now()'))
    created_by = Column(String, nullable=False)
    modified_date = Column(TIMESTAMP(timezone=True))
    modified_by = Column(String)
    description = Column(String)
    deviceid = Column(Text)
    reset_token = Column(String)
    reset_token_expiration = Column(TIMESTAMP(timezone=True))
    branch = relationship("UspBranch")
    role = relationship("UspRole")

class MenuPermission(Base):
    __tablename__ = 'menu_permission'

    id = Column(Integer,primary_key=True, nullable= False, autoincrement=True)
    pms_menu_name = Column(String,unique=True,nullable=False)
    pms_menu_level = Column(Integer,)
    pms_parent_id = Column(Integer)
    to_name = Column(String, unique=True, nullable=False)
    pms_menu_type = Column(Integer)
    pms_menu_index = Column(Integer)
    pms_menu_image = Column(String)
    created_date = Column(TIMESTAMP(timezone=True), server_default= text('now()'))
    created_by = Column(String)
    modified_date = Column(TIMESTAMP(timezone=True))
    modified_by = Column(String)
    db_id = Column(Integer)

class UspRuleNpmsAssign(Base):
    __tablename__ = 'usp_rule_npms_assign'

    id = Column(Integer, primary_key=True,nullable=False, autoincrement=True)
    roleid = Column(Integer, ForeignKey('usp_role.id'), nullable=False)
    pmsid = Column(Integer, ForeignKey('menu_permission.id'))
    p_view = Column(Boolean, server_default= text('false'))
    p_view_data = Column(Boolean,nullable=False, server_default= text('false'))
    p_refresh = Column(Boolean,nullable=False, server_default= text('false'))
    p_search = Column(Boolean,nullable=False, server_default= text('false'))
    p_add = Column(Boolean,nullable=False, server_default= text('false'))
    p_edit = Column(Boolean, nullable=False,server_default= text('false'))
    p_delete = Column(Boolean, nullable=False,server_default= text('false'))
    p_save = Column(Boolean,nullable=False, server_default= text('false'))
    p_print = Column(Boolean,nullable=False, server_default= text('false'))
    p_import = Column(Boolean,nullable=False, server_default= text('false'))
    p_export = Column(Boolean, nullable=False,server_default= text('false'))
    created_date = Column(TIMESTAMP(timezone=True), server_default= text('now()'))
    created_by = Column(String)
    modified_date = Column(Date)
    modified_by = Column(String)
    role = relationship("UspRole")
    menu = relationship("MenuPermission")

class Vote(Base):
    __tablename__ = "votes"
    post_id = Column(Integer, ForeignKey("posts.id",ondelete="CASCADE"),primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id",ondelete="CASCADE"),primary_key=True)

class Post(Base):
    __tablename__= "posts"

    id = Column(Integer,primary_key=True, nullable= False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default= 'True', nullable=False)
    create_date = Column(TIMESTAMP(timezone=True),nullable=False, server_default= text('now()'))
    owner_id  = Column(Integer, ForeignKey("users.id",ondelete="CASCADE"),nullable=False)
    owner = relationship("User")

# For Message
class Conversation(Base):
    __tablename__ = 'conversations'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String)
    type = Column(String)
    creation_timestamp = Column(TIMESTAMP(timezone=True))
    last_updated_timestamp = Column(TIMESTAMP(timezone=True))
    archived = Column(Boolean)
    muted = Column(Boolean)
    unread_messages_count = Column(Integer)
    visibility = Column(String)
    image_url = Column(String)
    description = Column(String)
    tags = Column(String)
    participants_limit = Column(Integer)
    moderators = Column(String)
    additional_settings = Column(JSONB)
    # messages = relationship("Message")

class Message(Base):
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    conversation_id = Column(Integer, ForeignKey('conversations.id', ondelete="CASCADE",onupdate="CASCADE"), nullable=False)
    sender_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    content = Column(Text)
    timestamp = Column(TIMESTAMP(timezone=True), server_default= text('now()'))
    conversation = relationship("Conversation")
    sender = relationship("User")

