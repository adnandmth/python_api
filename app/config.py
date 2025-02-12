import logging
from pydantic_settings import BaseSettings

# Configure logging for better debugging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

"""
📌 Pydantic Settings Configuration

✅ Uses `BaseSettings` from `pydantic_settings` to manage environment variables.
✅ Automatically validates and loads environment variables from `.env` file.
✅ Provides easy-to-use settings management for FastAPI applications.

🔹 Advantages:
- Keeps credentials and configurations **outside** the codebase.
- Automatically **validates** and **parses** environment variables.
- Supports **secrets management** in production environments (Heroku, AWS, etc.).
"""

class Settings(BaseSettings):
    """
    🔹 Settings class for managing environment variables.

    Environment variables required:
    - `database_hostname`: Hostname of the database server.
    - `database_port`: Port number for the database connection.
    - `database_password`: Password for the database user.
    - `database_name`: Name of the database.
    - `database_username`: Username for the database connection.
    - `secret_key`: Secret key used for authentication.
    - `algorithm`: Algorithm for token hashing (e.g., "HS256").
    - `access_token_expire_minutes`: Expiration time for access tokens (in minutes).
    """
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    class Config:
        """
        🔹 Configures Pydantic to load environment variables from a `.env` file.

        - In **development**, it reads from a local `.env` file.
        - In **production**, the hosting platform (Heroku, AWS, etc.) provides the environment variables.
        """
        env_file = ".env"


# ✅ Instantiate the settings object (Loads environment variables automatically)
settings = Settings()

# ✅ Log successful settings load
logger.info("Pydantic settings successfully loaded.")