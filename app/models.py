import logging
from sqlalchemy import Column, Integer, String
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import relationship
from .database import Base

# Configure logging for easier debugging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

"""
📌 ORM Models: SQLAlchemy + FastAPI

✅ Using SQLAlchemy ORM to define database tables as Python classes.
✅ Each model extends `Base` (from `declarative_base()`).
✅ Automatically maps classes to relational database tables.

🔹 Advantages:
- Simplifies database interactions using Python objects.
- Avoids writing raw SQL queries.
- Enables relationships between tables (ForeignKey, relationships).
"""

class User(Base):
    """
    Represents a table `users` in the database.

    Each user has:
    - `id`: Unique identifier (Primary Key).
    - `email`: Unique email address.
    - `password`: Hashed password (String).
    - `created_at`: Timestamp of user creation.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

    logger.info("User model initialized.")
    
class CallSentimentLog(Base):
    """
    Represents a table `call_sentiment_logs` in the database.

    Each log entry includes:
    - `id`: Auto-generated primary key.
    - `related_to_id`: Foreign key linking to Salesforce-related objects (e.g., Lead, Contact, Opportunity).
    - `call_id`: Unique identifier of the call (from Salesforce).
    - `overall_sentiment`: The aggregated sentiment result (positive, negative, neutral).
    - `created_at`: Timestamp of log entry creation.
    """
    __tablename__ = "call_sentiment_logs"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)  # Auto-incremented ID
    related_to_id = Column(String, nullable=False)  # Could be linked to Salesforce records
    call_id = Column(String, nullable=False, unique=True)  # Unique ID for the call
    overall_sentiment = Column(String, nullable=False)  # Sentiment analysis result
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))  # Auto-timestamp

    logger.info("CallSentimentLog model initialized.")
    
