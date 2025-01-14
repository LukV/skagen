import os
import logging
from typing import Callable
from email.message import EmailMessage
import smtplib
from pathlib import Path as PathLibPath
from fastapi import Path as FastAPIPath,Depends, HTTPException
import ulid
import requests
from core.auth import get_current_user
from sqlalchemy.orm import Session
from db import models
from db.database import get_db

logger = logging.getLogger(__name__)
path = PathLibPath(__file__).resolve().parent.parent

SES_SMTP_SERVER = os.getenv("SES_SMTP_SERVER")
SES_SMTP_PORT = int(os.getenv("SES_SMTP_PORT", "587"))
SES_SMTP_USERNAME = os.getenv("SES_SMTP_USERNAME")
SES_SMTP_PASSWORD = os.getenv("SES_SMTP_PASSWORD")
RESET_PASSWORD_URL = os.getenv("RESET_PASSWORD_URL")

def is_admin(
    current_user: models.User = Depends(get_current_user)
):
    """Evaluates if the logged in user has role admin."""
    if current_user.role != 'admin':
        raise HTTPException(status_code=403, detail="Admin privileges required")
    return current_user

def is_admin_or_entity_owner(
    entity_getter: Callable[[Session, str], models.Base], # type: ignore
    entity_name: str = "Entity",
    ownership_field: str = "user_id",
    entity_id_param: str = "entity_id",  # name of the parameter in the path
):
    """
    Returns a dependency that verifies if the current user is admin or
    the owner of the entity identified by `entity_id_param`.
    """

    async def dependency(
        entity_id: str = FastAPIPath(..., alias=entity_id_param),
        db: Session = Depends(get_db),
        current_user: models.User = Depends(get_current_user),
    ):
        if current_user.role == "admin":
            return current_user

        entity = entity_getter(db, entity_id)
        if not entity:
            raise HTTPException(status_code=404, detail=f"{entity_name} not found.")

        if getattr(entity, ownership_field) != current_user.id:
            raise HTTPException(status_code=403, detail="Operation not permitted.")

        return current_user

    return dependency

def generate_id(prefix: str) -> str:
    """
    Generates a unique ID with the given prefix.

    Args:
        prefix (str): A single character representing the entity type.

    Returns:
        str: The generated unique ID.
    """
    if len(prefix) != 1 or not prefix.isalpha() or not prefix.isupper():
        raise ValueError("Prefix must be a single uppercase letter.")
    return f"{prefix}{ulid.new()}"

def download_user_icon(url: str) -> str:
    """
    Downloads a user icon from the specified URL and saves it locally with a unique filename.

    Args:
        url (str): The URL of the user icon to download.
        user_id (str): The unique identifier of the user, used in the generated filename.

    Returns:
        str: The filename of the saved icon.
    """
    try:
        response = requests.get(url, stream=True, timeout=None)
        response.raise_for_status()

        content_type = response.headers.get('Content-Type', '')


        mime_to_extension = {
            "image/jpeg": "jpg",
            "image/png": "png",
            "image/gif": "gif",
            "image/webp": "webp",
        }
        file_extension = mime_to_extension.get(content_type, "png")  # Default to 'png' if unknown


        icon_filename = f"{generate_id('A')}.{file_extension}"
        icon_path = PathLibPath(path / f"static/icons/{icon_filename}")
        icon_path.parent.mkdir(parents=True, exist_ok=True)

        with open(icon_path, "wb") as icon_file:
            for chunk in response.iter_content(1024):
                icon_file.write(chunk)

        return icon_filename

    except requests.RequestException as exc:
        return str(exc)

def send_reset_email(email: str, token: str):
    """Sends a password reset email to the specified recipient."""
    reset_link = f"{RESET_PASSWORD_URL}?token={token}"

    msg = EmailMessage()
    msg["Subject"] = "Password Reset Request"
    msg["From"] = "dataframe.one@gmail.com"
    msg["To"] = email
    msg.set_content(f"Click the following link to reset your password: {reset_link}")

    try:
        with smtplib.SMTP(SES_SMTP_SERVER, SES_SMTP_PORT) as server:
            server.starttls()  # Secure the connection
            server.login(SES_SMTP_USERNAME, SES_SMTP_PASSWORD)
            server.send_message(msg)
        logger.info("Password reset email sent successfully.")
    except smtplib.SMTPException as smtp_error:
        logger.error("SMTP error occurred while sending email to %s: %s",
                     email, smtp_error)
        raise
    except Exception as general_error:
        logger.error("Unexpected error occurred while sending email to %s: %s",
                     email, general_error)
        raise
