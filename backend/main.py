import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from fastapi import FastAPI # pylint: disable=C0413
from fastapi.staticfiles import StaticFiles # pylint: disable=C0413
from core.logging import configure_logging # pylint: disable=C0413
from core.config import setup_cors # pylint: disable=C0413
from routers import users, auth, hypothesis # pylint: disable=C0413
from db.database import Base, engine # pylint: disable=C0413

# Configure logging
configure_logging()

# Create FastAPI app instance
app = FastAPI()

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize configurations
setup_cors(app)

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(hypothesis.router, prefix="/claims", tags=["claims"])

# Mount the static images directory at "/icons"
static_icons_dir = os.path.join(os.path.dirname(__file__), "static", "avatars")
app.mount("/avatars", StaticFiles(directory=static_icons_dir), name="avatars")
