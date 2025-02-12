from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import engine
from .routers import user, auth, speech

"""
This app uses Alembic for database migrations, so automatic table creation
via SQLAlchemy's `create_all` is not required.

To run the FastAPI server, use the following command:
  uvicorn {module_name}:{app_instance} --reload

- `--reload` enables auto-reloading when code changes.
"""
# models.Base.metadata.create_all(bind=engine)  # Uncomment if not using Alembic

# Initialize FastAPI instance
app = FastAPI()

# Allow all origins for CORS (adjust for production security)
origins = ["*"] 
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
        
# Include routers for different app modules
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(speech.router)

@app.get("/")
def root():
    return {"message": "alive"}
