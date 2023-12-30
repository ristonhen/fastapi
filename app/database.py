from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from .config import settings
# SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:123@localhost/fastapi'

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'
engine =create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# def switch_database_backend(database_backend):
#     global engine, SessionLocal

#     if database_backend == "oracle":
#         # Configure Oracle backend
#         # Set the appropriate connection string for Oracle
#         SQLALCHEMY_DATABASE_URL = "oracle://user:password@hostname:port/service_name"
#         engine = create_engine(SQLALCHEMY_DATABASE_URL)
#     elif database_backend == "mysql":
#         # Configure MySQL backend
#         SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'
#         engine = create_engine(SQLALCHEMY_DATABASE_URL)
#     elif database_backend == "postgres":
#         # Configure PostgreSQL backend
#         SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'
#         engine = create_engine(SQLALCHEMY_DATABASE_URL)
#     else:
#         raise ValueError("Invalid database backend specified.")

#     # Create the session factory
#     SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# # Set the default database to PostgreSQL
# default_database_backend = "postgres"
# switch_database_backend(default_database_backend)




Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# while True:
#     try:
#         conn = psycopg2.connect(
#             host='localhost',
#             database='fastapi',
#             user='postgres', 
#             password='123',
#             cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("Database connection was succesfully!")
#         break
#     except Exception as error:
#         print("Connection to database error")  
#         print("Error:", error)  
#         time.sleep(2)
