from fastapi import APIRouter, UploadFile, File, HTTPException, status, Depends
import logging
from .. import models, schemas, oauth2
from google.cloud import speech
from textblob import TextBlob
from googletrans import Translator
from typing import List
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter(
    prefix="/speech",
    tags=["speech"]
)

translator = Translator()

@router.post("/transcribe", response_model=schemas.TranscriptionResponse, status_code=status.HTTP_201_CREATED)
async def transcribe_audio(
    file: UploadFile = File(...), db: Session = Depends(get_db)
):
    """Transcribe, analyze sentiment, store in DB, and return structured data."""
    try:
        audio_bytes = await file.read()
        transcriptions = transcribe_audio_from_bytes(audio_bytes)

        # Generate structured responses
        speech_transcriptions = [
            schemas.SpeechTranscription(
                transcription=text,
                sentiment=analyze_sentiment(text)
            ) for text in transcriptions
        ]

        # Calculate overall sentiment
        overall_sentiment = calculate_overall_sentiment([t.sentiment for t in speech_transcriptions])

        # Mock Salesforce-related ID and Call ID
        related_to_id = "SF12345"  # Replace with actual related ID from request
        call_id = file.filename  # Use filename as call ID (or parse from metadata)

        # Save to database
        new_log = save_transcription_to_db(db, related_to_id, call_id, overall_sentiment)
        print(f'new log: {new_log}')

        # Construct response
        response = schemas.TranscriptionResponse(
            filename=file.filename,
            transcriptions=speech_transcriptions,
            overall_sentiment=overall_sentiment
        )

        logging.info(f"API Response: {response.json()}")
        return response

    except Exception as e:
        logging.error(f"Error processing file {file.filename}: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
# ========================= HELPER FUNCTIONS ========================= #
    
def analyze_sentiment(text: str):
    """Analyze sentiment of text using TextBlob."""
    try:
        translated_text = translator.translate(text, src="id", dest="en").text  # Translate to English
        blob = TextBlob(translated_text)
        sentiment_score = blob.sentiment.polarity  # Score from -1 (negative) to +1 (positive)

        sentiment = "positive" if sentiment_score > 0 else "negative" if sentiment_score < 0 else "neutral"
        return schemas.SentimentAnalysis(sentiment=sentiment, score=sentiment_score)
    except Exception as e:
        logging.error(f"Sentiment analysis error: {e}")
        return schemas.SentimentAnalysis(sentiment="neutral", score=0.0)

def transcribe_audio_from_bytes(audio_bytes: bytes) -> List[str]:
    """Transcribe speech from an audio file using Google Speech-to-Text API."""
    client = speech.SpeechClient()

    audio = speech.RecognitionAudio(content=audio_bytes)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="id-ID"  # Bahasa Indonesia
    )

    response = client.recognize(config=config, audio=audio)
    logging.info(f"Speech-to-Text response: {response}")

    return [result.alternatives[0].transcript for result in response.results]

def calculate_overall_sentiment(sentiments: List[schemas.SentimentAnalysis]) -> schemas.OverallSentiment:
    total_score = sum(s.score for s in sentiments)
    avg_score = total_score / len(sentiments) if sentiments else 0  # Avoid division by zero

    overall_sentiment = "positive" if avg_score > 0 else "negative" if avg_score < 0 else "neutral"
    
    return schemas.OverallSentiment(overall_sentiment=overall_sentiment, average_score=avg_score)

def save_transcription_to_db(
    db: Session, related_to_id: str, call_id: str, overall_sentiment: str
):
    """
    Saves transcription sentiment results to the database.
    """
    new_log = models.CallSentimentLog(
        related_to_id=related_to_id,
        call_id=call_id,
        overall_sentiment=overall_sentiment
    )
    
    db.add(new_log)
    db.commit()
    db.refresh(new_log)
    return new_log