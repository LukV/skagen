from pathlib import Path
import ulid
import requests
from fastapi import Depends, HTTPException
from core.auth import get_current_user
from db import models

path = Path(__file__).resolve().parent.parent

def is_admin(
    current_user: models.User = Depends(get_current_user)
):
    """Evaluates if the logged in user has role admin."""
    if current_user.role != 'admin':
        raise HTTPException(status_code=403, detail="Admin privileges required")
    return current_user

def is_admin_or_owner(
    user_id: str,
    current_user: models.User = Depends(get_current_user)
):
    """Evaluates if the logged in user had rights to the involved object or method."""
    if current_user.role == 'admin' or current_user.id == user_id:
        return current_user

    raise HTTPException(status_code=403, detail="Operation not permitted")

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
        icon_path = Path(path / f"static/icons/{icon_filename}")
        icon_path.parent.mkdir(parents=True, exist_ok=True)

        with open(icon_path, "wb") as icon_file:
            for chunk in response.iter_content(1024):
                icon_file.write(chunk)

        return icon_filename

    except requests.RequestException as exc:
        return exc
