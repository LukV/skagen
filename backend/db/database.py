import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import dotenv

# PostgreSQL database connection URL
dotenv.load_dotenv()
SQLALCHEMY_DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL")

# Initialize the engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Configure SessionLocal and Base
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    """Yields a new database session for request lifecycle management."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
