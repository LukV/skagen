from typing import List
from fastapi import APIRouter, BackgroundTasks, File, HTTPException, Depends, UploadFile
from sqlalchemy.orm import Session
from crud import users as crud_users
from schemas import users as user_schemas
from db.database import get_db

router = APIRouter()

@router.post("/", response_model=user_schemas.UserResponse)
def create_user(user: user_schemas.UserCreate, db: Session = Depends(get_db)):
    """Create a new user in the database."""
    if crud_users.get_user_by_email(db, user.email):
        raise HTTPException(status_code=400, detail="Username or email already registered.")
    return crud_users.create_user(db, user)

@router.get("/", response_model=List[user_schemas.UserResponse])
def get_all_users(db: Session = Depends(get_db)):
    """Retrieve a list of all users in the database."""
    return crud_users.get_all_users(db)

@router.get("/{user_id}", response_model=user_schemas.UserResponse)
def get_user(user_id: str, db: Session = Depends(get_db)):
    """Update an existing user's details."""
    return crud_users.get_user_by_id(db, user_id)

@router.put("/{user_id}", response_model=user_schemas.UserResponse)
def update_user(user_id: str, user_update: user_schemas.UserUpdate, db: Session = Depends(get_db)):
    """Update an existing user's details."""
    return crud_users.update_user(db, user_id, user_update)

@router.delete("/{user_id}")
def delete_user(user_id: str, db: Session = Depends(get_db)):
    """Delete an existing user from the database. This is a hard delete."""
    crud_users.delete_user(db, user_id)
    return "User deleted successfully"

@router.put("/{user_id}/icon")
def upload_icon(
    user_id: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    background_tasks: BackgroundTasks = BackgroundTasks(),
):
    """Upload or replace a user's profile icon."""
    return crud_users.update_user_icon(
        db=db,
        user_id=user_id,
        file=file,
        background_tasks=background_tasks,
    )
