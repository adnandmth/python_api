import logging
from pydantic import BaseModel, EmailStr, Field, ValidationError
from datetime import datetime
from typing import Annotated, List, Optional

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

"""
This module contains Pydantic models for request validation and data transfer.

- Extends Pydantic's `BaseModel` to validate incoming data.
- Ensures API requests conform to expected formats.
- Improves error handling and debugging.

Pydantic automatically validates and converts incoming data before it reaches business logic.
"""
class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        """Enable ORM compatibility."""
        from_attributes = True
    
class UserCreate(BaseModel):
    email: EmailStr 
    password: str

    def log_data(self):
        logger.info(f"User Registration - Email: {self.email}")
        
class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    
class TokenData(BaseModel):
    id: Optional[str] = None  # ID might be missing if token is invalid
      
class SentimentAnalysis(BaseModel):
    sentiment: str = Field(..., example="positive")  # Can be positive, negative, or neutral
    score: float = Field(..., example=0.7)  # Sentiment score (-1 to +1)
    
class SpeechTranscription(BaseModel):
    transcription: str = Field(..., example="Halo selamat sore")  # The transcribed text
    sentiment: SentimentAnalysis  # Link transcription with sentiment

class OverallSentiment(BaseModel):
    overall_sentiment: str = Field(..., example="positive")  # Overall sentiment classification
    average_score: float = Field(..., example=0.4667)  # Average sentiment score

class TranscriptionResponse(BaseModel):
    filename: str = Field(..., example="test.wav")  # Name of the uploaded file
    transcriptions: List[SpeechTranscription]  # List of transcribed lines with sentiment
    overall_sentiment: OverallSentiment  # Aggregated sentiment of the call