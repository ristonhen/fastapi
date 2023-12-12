from pydantic import BaseSettings

class Setting(BaseSettings):
    database_hostname: str
    hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    database_port_mysql: str
    # database_backend: str # Add the database setting

    class Config:
        env_file = ".env"
settings = Setting()