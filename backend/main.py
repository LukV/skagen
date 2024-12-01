import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from core.logging import configure_logging
from core.config import setup_cors
from routers import users, auth

# Configure logging
configure_logging()

# Create FastAPI app instance
app = FastAPI()

# Initialize configurations
setup_cors(app)

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(users.router, prefix="/users", tags=["users"])

# Mount the static images directory at "/icons"
static_icons_dir = os.path.join(os.path.dirname(__file__), "static", "avatars")
app.mount("/avatars", StaticFiles(directory=static_icons_dir), name="avatars")
