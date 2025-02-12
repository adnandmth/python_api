import logging
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

"""
📌 ORMs (Object-Relational Mappers)
FastAPI works with any database and supports multiple database libraries.

One of the most common approaches is using an "ORM" (Object-Relational Mapper).
An ORM provides tools to map objects in Python code to tables in a SQL database.

✅ Benefits of using an ORM:
- Automatically converts Python objects into database rows/columns.
- Reduces SQL query complexity.
- Improves maintainability and security.

🔹 SQLAlchemy is one of the most widely used ORMs in FastAPI.
"""

# ✅ Database Connection Configuration
"""
📌 IMPORTANT:
Using Heroku means the database instance is managed under the Heroku app.

⚠️ Production Setup:
- The app retrieves database credentials from the **Heroku app environment variables**.
- Local development uses the `settings` module to fetch database credentials from **config.py**.

Heroku App: https://dashboard.heroku.com/apps/pythonapi-adnandmth/settings
"""

# Construct the database URL dynamically (works for both local & production)
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

# ✅ Create a new database engine using SQLAlchemy
"""
The `create_engine` function initializes the database connection.
- The `SQLALCHEMY_DATABASE_URL` specifies the database type (PostgreSQL) and connection details.
"""
engine = create_engine(SQLALCHEMY_DATABASE_URL)
logger.info("Database engine initialized.")

# ✅ Create a database session
"""
`SessionLocal` is a factory for new database session instances.

- `autocommit=False`: Ensures transactions are explicitly committed.
- `autoflush=False`: Prevents automatic flushing of changes.
- `bind=engine`: Links the session with the database engine.
"""
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ✅ Create a base class for ORM models
"""
`Base` is a class from which all ORM models will inherit.
Each model will represent a database table.
"""
Base = declarative_base()
 
# ✅ Dependency: Database Session Generator
"""
📌 `get_db()` - Dependency Injection for Database Sessions

- Each request gets a new database session instance.
- The session is closed automatically once the request is completed.
- This prevents memory leaks and ensures efficient database connections.

Usage in FastAPI routes:
"""
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        logger.info("Database session closed.")