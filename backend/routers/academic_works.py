from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from crud import academic_works as crud_academic_works
from schemas import academic_works as academic_work_schemas
from schemas.common import PaginatedResponse
from db.database import get_db
from db import models
from core.auth import get_current_user

router = APIRouter()

@router.get("/", response_model=PaginatedResponse)
def get_all_academic_works(
    db: Session = Depends(get_db),
    _current_user: models.User = Depends(get_current_user),
    page: int = Query(1, ge=1, description="Page number (1-based index)"),
    per_page: int = Query(10, ge=1, le=100, 
                          description="Number of records per page (max 100)"),
):
    """
    Retrieve a paginated list of academic works.

    Query Parameters:
        page (int): The page number to retrieve.
        per_page (int): The number of items per page.
    """
    paginated_works = crud_academic_works.get_all_academic_works(db, page=page, per_page=per_page)

    return {
        "total_pages": paginated_works["total_pages"],
        "total_items": paginated_works["total_items"],
        "current_page": paginated_works["current_page"],
        "items": [
            academic_work_schemas.AcademicWorkResponse(**academic_work.__dict__)
            for academic_work in paginated_works["items"]
        ],
    }

@router.get("/{academic_work_id}", response_model=academic_work_schemas.AcademicWorkResponse)
def get_academic_work(
    academic_work_id: str,
    db: Session = Depends(get_db)
):
    """Retrieve a academic_work's details."""
    academic_work = crud_academic_works.get_academic_work_by_id(db, academic_work_id)
    if not academic_work:
        raise HTTPException(status_code=404, detail="academic_work not found")

    return academic_work_schemas.AcademicWorkResponse(**academic_work.__dict__)
