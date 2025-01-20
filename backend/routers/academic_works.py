from fastapi import APIRouter, HTTPException, Depends, Query, BackgroundTasks
from sqlalchemy.orm import Session
from core.utils import is_admin
from core.auth import get_current_user
from crud import academic_works as crud_academic_works
from schemas import academic_works as academic_work_schemas
from schemas.common import PaginatedResponse
from db.database import get_db
from db import models

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

@router.put("/{academic_work_id}", response_model=academic_work_schemas.AcademicWorkResponse)
def update_academic_work(
    academic_work_id: str,
    academic_work_update: academic_work_schemas.AcademicWorkUpdate,
    db: Session = Depends(get_db),
    _current_user: models.User = Depends(get_current_user),
):
    """Update an academic work by ID."""
    academic_work = crud_academic_works.get_academic_work_by_id(db, academic_work_id)
    if not academic_work:
        raise HTTPException(status_code=404, detail="Academic work not found")

    updated_academic_work = crud_academic_works.update_academic_work(
        db,
        academic_work_id,
        academic_work_update
    )
    return academic_work_schemas.AcademicWorkResponse(**updated_academic_work.__dict__)

@router.post("/update-llm-extended-summaries")
def update_all_llm_extended_summaries(
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    _current_user: models.User = Depends(is_admin),
):
    """Run a background task to update all llm_extended_summary fields that are null."""
    background_tasks.add_task(crud_academic_works.update_null_llm_extended_summaries, db)
    return {"message": "Background task to update llm_extended_summaries started."}
