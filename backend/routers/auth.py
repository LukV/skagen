from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from schemas.auth import TokenPair, LoginRequest, GoogleLoginRequest
from schemas.users import UserCreate
from db.database import get_db
from crud import users as crud_users
from core import auth, utils

router = APIRouter()

@router.post("/login", response_model=TokenPair)
def login(
    login_data: LoginRequest,
    db: Session = Depends(get_db)
):
    """Endpoint for user login with credentials."""
    if not login_data.username or not login_data.password:
        raise HTTPException(
            status_code=400,
            detail="Invalid credentials."
        )

    user = crud_users.get_user_by_email(db, login_data.username)

    if not user or not auth.verify_password(login_data.password, user.password):
        raise HTTPException(
            status_code=400,
            detail="Invalid credentials."
        )

    access_token = auth.create_access_token(data={"sub": user.email})
    refresh_token = auth.create_refresh_token(data={"sub": user.email}) # pylint: disable=W0621
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@router.post("/login/google", response_model=TokenPair)
def google_login(
    google_login_data: GoogleLoginRequest,
    db: Session = Depends(get_db)
):
    """Endpoint for user login with Google account."""
    token = google_login_data.token

    google_user_data = auth.verify_google_token(token)
    user = crud_users.get_user_by_email(db, google_user_data["email"])
    google_picture_url = google_user_data.get("picture")

    if not user:
        icon_path = utils.download_user_icon(google_picture_url) \
                        if google_picture_url else None
        new_user_data = UserCreate(
            username=google_user_data["name"],
            email=google_user_data["email"],
            icon=icon_path
        )
        user = crud_users.create_user(db, user=new_user_data)

    # Generate access and refresh tokens
    access_token = auth.create_access_token(data={"sub": user.email})
    refresh_token = auth.create_refresh_token(data={"sub": user.email}) # pylint: disable=W0621
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@router.post("/refresh", response_model=TokenPair)
def refresh_token(token: str, db: Session = Depends(get_db)):
    """Refreshes the access token using a valid refresh token."""
    try:
        payload = jwt.decode(token, auth.SECRET_KEY, algorithms=[auth.ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise HTTPException(
                status_code=401,
                detail={
                    "code": "AUTH_005",
                    "message": "Invalid refresh token."
                })

        user = crud_users.get_user_by_email(db, email)
        if user is None:
            raise HTTPException(
                status_code=401,
                detail={
                    "code": "USER_001",
                    "message": "User not found."
                })

        # Generate new access and refresh tokens
        access_token = auth.create_access_token(data={"sub": email})
        new_refresh_token = auth.create_refresh_token(data={"sub": email})
        return {
            "access_token": access_token,
            "refresh_token": new_refresh_token,
            "token_type": "bearer"
        }

    except JWTError as exc:
        raise HTTPException(
            status_code=401,
            detail={
                "code": "AUTH_005",
                "message": "Invalid refresh token.",
                "msgtype": "error"
            }) from exc
