from pydantic import BaseSettings


class Settings(BaseSettings):
    database_secret_key:str="09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    
    database_algorithm:str="HS256"
    database_expire_time:int=100
    database_username:str="postgres"
    database_password:str="Vikash123"
    database_hostname:str="localhost"
    database_name:str="fastapi"
    database_port:str="5432"

    class Config:
        env_file=".env"

settings=Settings()