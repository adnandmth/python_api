from pydantic_settings import BaseSettings

"""
Pydantic Settings provides optional Pydantic features for loading a settings or config class from environment variables or secrets files.

BaseSettings provides an inheritance from pydantic model that handles setting validation from the given properties
"""
class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    # tells pydantic to import the ENV setting file
    class Config:
        env_file = ".env" # name of the file containing the ENVs

# instantiate an object of class Settings
settings = Settings()