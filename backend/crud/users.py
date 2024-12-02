import os
from pathlib import Path
import shutil
from typing import List, Optional
from fastapi import BackgroundTasks, HTTPException, UploadFile, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from schemas import users as user_schemas
from db import models
from core import auth, utils


BASE_DIR = Path(__file__).resolve().parent.parent
ICON_DIR = BASE_DIR / "static/icons"
ICON_DIR.mkdir(parents=True, exist_ok=True)

def create_user(
    db: Session,
    user: user_schemas.UserCreate
) -> models.User:
    """
    Creates a new user in the database.
    """
    hashed_password = auth.hash_password(user.password) if user.password else None
    user_id = utils.generate_id('U')
    db_user = models.User(
        id=user_id,
        username=user.username,
        email=user.email,
        password=hashed_password,
        icon=user.icon
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(
    db: Session,
    user_id: str,
    user_update: user_schemas.UserUpdate
) -> models.User:
    """
    Updates an existing user's details in the database.
    """
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found.")
    update_data = user_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_user, key, value)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_password(
    db: Session,
    user_id: str,
    new_password: str
) -> models.User:
    """
    Updates an existing user's password in the database.
    """
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found.")
    try:
        hashed_password = auth.hash_password(new_password)
        db_user.password = hashed_password
        db.commit()
        db.refresh(db_user)
    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected database error occurred."
        ) from exc
    return db_user

def update_user_icon(
    db: Session,
    user_id: str,
    file: UploadFile,
    background_tasks: BackgroundTasks
) -> dict:
    """
    Updates a user's profile icon.
    """
    db_user = get_user_by_id(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found.")

    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Uploaded file must be an image.")

    file_extension = file.filename.split(".")[-1]
    unique_filename = f"{utils.generate_id('A')}.{file_extension}"
    file_path = ICON_DIR / unique_filename

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    if db_user.icon:
        old_icon_path = ICON_DIR / db_user.icon
        if old_icon_path.exists():
            background_tasks.add_task(os.remove, old_icon_path)

    db_user.icon = unique_filename
    db.commit()
    db.refresh(db_user)

    return db_user

def delete_user(db: Session, user_id: str) -> Optional[models.User]:
    """
    Deletes an existing user from the database.

    Args:
        db (Session): The database session.
        user_id (int): The ID of the user to delete.

    Returns:
        User or None: The deleted user instance or None if not found.
    """
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        if db_user.icon:
            background_tasks = BackgroundTasks()
            icon_path = ICON_DIR / db_user.icon
            if icon_path.exists():
                background_tasks.add_task(os.remove, icon_path)

        db.delete(db_user)
        db.commit()
    return db_user

def get_all_users(db: Session) -> List[models.User]:
    """
    Retrieves all users from the database.
    """
    return db.query(models.User).all()

def get_user_by_id(db: Session, user_id: str) -> Optional[models.User]:
    """
    Fetches a user by their id.
    """
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str) -> Optional[models.User]:
    """
    Fetches a user by their email.
    """
    return db.query(models.User).filter(models.User.email == email).first()
