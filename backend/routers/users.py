from typing import List
from fastapi import APIRouter, BackgroundTasks, File, HTTPException, Depends, UploadFile, status
from sqlalchemy.orm import Session
from crud import users as crud_users
from schemas import users as user_schemas
from db.database import get_db
from db import models
from core.auth import get_current_user, hash_password, SECRET_KEY, ALGORITHM, create_password_reset_token
from core.utils import is_admin, is_admin_or_entity_owner, send_reset_email
from jose import jwt

router = APIRouter()

@router.post("/", response_model=user_schemas.UserResponse)
def create_user(
    user: user_schemas.UserCreate,
    db: Session = Depends(get_db)
    ):
    """Create a new user in the database."""
    if crud_users.get_user_by_email(db, user.email) or \
        crud_users.get_user_by_username(db, user.username):
        raise HTTPException(status_code=400, detail="Username or email already registered.")
    return crud_users.create_user(db, user)

@router.get("/", response_model=List[user_schemas.UserResponse])
def get_all_users(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Retrieve a list of all users in the database."""
    users = crud_users.get_all_users(db)
    if current_user.role == 'admin': # type: ignore
        return [user_schemas.AdminUserResponse(**user.__dict__) for user in users]

    return [user_schemas.UserResponse(**user.__dict__) for user in users]

@router.get("/me", response_model=user_schemas.UserResponse)
def get_current_user_info(
    current_user: models.User = Depends(get_current_user)
):
    """Retrieve the current user's information."""
    if current_user.role == 'admin': # type: ignore
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
    if current_user.role == 'admin': # type: ignore
        return user_schemas.AdminUserResponse(**user.__dict__)

    return user_schemas.UserResponse(**user.__dict__)

@router.put("/{user_id}", response_model=user_schemas.UserResponse)
def update_user(
    user_id: str,
    user_update: user_schemas.UserUpdate,
    db: Session = Depends(get_db),
    _current_user: models.User = Depends(
        is_admin_or_entity_owner(
            crud_users.get_user_by_id,
            entity_name="Hypothesis",
            ownership_field="id",
            entity_id_param="hypothesis_id",
        )
    )

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

@router.post("/request-password-reset")
def request_password_reset(
    payload: user_schemas.PasswordResetRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Request a password reset by sending a reset link to the user's email. 
    Relies on a utility function tied to a specific smtp service, eg AWS SES.
    See GH for details.
    """
    user = crud_users.get_user_by_email(db, email=payload.email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    # Generate a token with an expiry
    token = create_password_reset_token(user.id)

    # Add the email sending task to the background
    background_tasks.add_task(send_reset_email, payload.email, token)

    return "Password reset email sent."

@router.post("/reset-password")
def reset_password(
    payload: user_schemas.PasswordReset,
    db: Session = Depends(get_db)
):
    """Reset a user's password using a token for validation."""
    try:
        # Decode the token using the auth module
        payload_data = jwt.decode(payload.token, SECRET_KEY, algorithms=[ALGORITHM])
        user_uid = payload_data.get("sub")
    except jwt.JWTError as exc:
        raise HTTPException(status_code=400, detail="Invalid or expired token.") from exc

    # Verify that the email and user_uid match
    user = crud_users.get_user_by_email(db, email=payload.email)
    if not user or str(user.id) != user_uid:
        raise HTTPException(status_code=404,
                            detail="User not found, or email does not match token.")

    user.password = hash_password(payload.new_password)
    db.commit()
    return {
        "detail": "Password reset successfully",
    }

@router.post("/change-password")
def change_password(
    request: user_schemas.PasswordChange,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Endpoint to update the password for the authenticated user."""
    updated_user = crud_users.update_password(
        db=db,
        user_id=current_user.id,
        new_password=request.new_password
    )
    if not updated_user:
        raise HTTPException(status_code=404,
                            detail="User not found or password could not be updated.")
    return "Password updated successfully."
