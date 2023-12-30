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

    
    """
    tells pydantic to import the ENV setting file

    In the production, this reference will be replaced by the hosting env variables,
    since we don't include the local ENV into the remote repositories

    Since our app is based on Heroku, it knows how to fetch the VARs into this setting class.
    This is can be achieved using this pydantic library that checks any dependencies required by the class
    """
    class Config:
        env_file = ".env" # name of the file containing the ENVs

# instantiate an object of class Settings
settings = Settings()