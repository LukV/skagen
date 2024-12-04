from typing import List
from fastapi import APIRouter, BackgroundTasks, File, HTTPException, Depends, UploadFile, status
from sqlalchemy.orm import Session
from crud import users as crud_users
from schemas import users as user_schemas
from db.database import get_db
from db import models
from core.auth import get_current_user
from core.utils import is_admin, is_admin_or_owner

router = APIRouter()

@router.post("/", response_model=user_schemas.UserResponse)
def create_user(
    user: user_schemas.UserCreate,
    db: Session = Depends(get_db)
    ):
    """Create a new user in the database."""
    if crud_users.get_user_by_email(db, user.email):
        raise HTTPException(status_code=400, detail="Username or email already registered.")
    return crud_users.create_user(db, user)

@router.get("/", response_model=List[user_schemas.UserResponse])
def get_all_users(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Retrieve a list of all users in the database."""
    users = crud_users.get_all_users(db)
    if current_user.role == 'admin':
        return [user_schemas.AdminUserResponse(**user.__dict__) for user in users]

    return [user_schemas.UserResponse(**user.__dict__) for user in users]

@router.get("/me", response_model=user_schemas.UserResponse)
def get_current_user_info(
    current_user: models.User = Depends(get_current_user)
):
    """Retrieve the current user's information."""
    if current_user.role == 'admin':
        return user_schemas.AdminUserResponse(**current_user.__dict__)

    return user_schemas.UserResponse(**current_user.__dict__)

@router.get("/{user_id}", response_model=user_schemas.UserResponse)
def get_user(
    user_id: str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Retrieve a user's details."""
    user = crud_users.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if current_user.role == 'admin':
        return user_schemas.AdminUserResponse(**user.__dict__)

    return user_schemas.UserResponse(**user.__dict__)

@router.put("/{user_id}", response_model=user_schemas.UserResponse)
def update_user(
    user_id: str,
    user_update: user_schemas.UserUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(is_admin_or_owner)  # pylint: disable=W0613
):
    """Update an existing user's details."""
    return crud_users.update_user(db, user_id, user_update)

@router.put("/{user_id}/icon")
def upload_icon(
    user_id: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    background_tasks: BackgroundTasks = BackgroundTasks(),
    current_user: models.User = Depends(get_current_user) # pylint: disable=W0613
):
    """Upload or replace a user's profile icon."""
    return crud_users.update_user_icon(
        db=db,
        user_id=user_id,
        file=file,
        background_tasks=background_tasks,
    )

@router.put("/{user_id}/role", response_model=user_schemas.AdminUserResponse)
def update_user_role(
    user_id: str,
    user_update: user_schemas.AdminUserUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(is_admin)  # pylint: disable=W0613
):
    """Admin can update a user's role."""
    return crud_users.admin_update_user(db, user_id, user_update)

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)  # pylint: disable=W0613
):
    """Delete an existing user from the database. This is a hard delete."""
    crud_users.delete_user(db, user_id)
