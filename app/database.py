"""
ORMs
FastAPI works with any database and any style of library to talk to the database.

A common pattern is to use an "ORM": an "object-relational mapping" library.

An ORM has tools to convert ("map") between objects in code and database tables ("relations").

With an ORM, you normally create a class that represents a table in a SQL database, each attribute of the class represents a column, with a name and a type.

sqlalchemy is one of the libraries that support this ORMs

"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings
# import psycopg2 as psy
# import time
# from psycopg2.extras import RealDictCursor

# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://<username>:<password>@<ip address/hostname>/<db_name>"
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base() # extending declarative base class
 
"""
get_db from database is the base of database creation and connection
engine is where the database engine was setup.

Instantiate the session.

Each instance of the SessionLocal class will be a database session. The class itself is not a database session yet.

But once we create an instance of the SessionLocal class, this instance will be the actual database session.
"""
def get_db():
    db = SessionLocal() # get the connected DB
    try:
        yield db
    finally:
        db.close()

"""
connecting to the postgres DB

We put it inside a while loop to handle data connection issue.
It will keep calling the DB until it was successfully connected

Add a time to give a buffer before the next attempt is conducted
"""
# while True:

#     try:
#         conn = psy.connect(
#             host='localhost',
#             database='python_api',
#             user='postgres',
#             password='jerapah102938',
#             cursor_factory=RealDictCursor
#         )
#         cursor = conn.cursor()
#         print("Database connection was successfully connected")
#         break
#     except Exception as error:
#         print(f"Failed connecting the database --- {error}")
#         time.sleep(2) # 2 seconds sleep