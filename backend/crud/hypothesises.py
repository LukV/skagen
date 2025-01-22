from typing import List, Optional, Tuple
from fastapi import HTTPException
from sqlalchemy import asc, desc
from sqlalchemy.orm import Session
from sqlalchemy_pagination import paginate
from schemas import hypothesises as hypothesis_schemas
from db import models
from core import utils

def create_hypothesis(
    db: Session,
    hypothesis: hypothesis_schemas.HypothesisCreate,
    current_user: models.User
) -> models.Hypothesis:
    """
    Creates a new hypothesis in the database.
    """
    hypothesis_id = utils.generate_id('H')
    db_hypothesis = models.Hypothesis(
        id=hypothesis_id,
        user_id=current_user.id,
        parent_id=None,
        content=hypothesis.content,
        extracted_topics=[],
        extracted_terms=[],
        query_type='unknown'
    )
    db.add(db_hypothesis)
    db.commit()
    db.refresh(db_hypothesis)
    return db_hypothesis

def update_hypothesis(
    db: Session,
    hypothesis_id: str,
    hypothesis_update: hypothesis_schemas.HypothesisUpdate
) -> Tuple[models.Hypothesis, bool]:
    """
    Updates an existing hypothesis's details in the database.
    """
    db_hypothesis = db.query(models.Hypothesis) \
        .filter(models.Hypothesis.id == hypothesis_id).first()
    if not db_hypothesis:
        raise HTTPException(status_code=404, detail="Hypothesis not found.")

    is_content_updated = bool(
        hypothesis_update.content and hypothesis_update.content != db_hypothesis.content
    )

    update_data = hypothesis_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_hypothesis, key, value)

    db.commit()
    db.refresh(db_hypothesis)

    return db_hypothesis, is_content_updated

def delete_hypothesis(db: Session, hypothesis_id: str) -> Optional[models.Hypothesis]:
    """
    Deletes an existing hypothesis from the database.

    Args:
        db (Session): The database session.
        hypothesis_id (int): The ID of the hypothesis to delete.

    Returns:
        hypothesis or None: The deleted hypothesis instance or None if not found.
    """
    db_hypothesis = db.query(models.Hypothesis) \
        .filter(models.Hypothesis.id == hypothesis_id).first()
    if db_hypothesis:
        db.delete(db_hypothesis)
        db.commit()
    return db_hypothesis

def get_all_hypothesises(
        db: Session,
        current_user: models.User,
        page: int,
        per_page: int,
        sort_by: Optional[str] = None,
        sort_order: Optional[str] = "asc",
        filters: Optional[dict] = None) -> dict:
    """
    Retrieves all hypotheses from the database with optional sorting and filtering.

    Parameters:
        sort_by (str): The field to sort by.
        sort_order (str): The sort order ('asc' or 'desc').
        filters (dict): Dictionary of filters where keys are fields and values are filter values.
    """
    if current_user.role == 'admin':  # pylint: disable=E1136
        query = db.query(models.Hypothesis)
    else:
        query = db.query(models.Hypothesis).filter(
            models.Hypothesis.user_id == current_user.id)

    # Apply filters
    if filters:
        for key, value in filters.items():
            if key == "content":
                query = query.filter(getattr(models.Hypothesis, key).contains(value))
            else:  # Default exact match
                query = query.filter(getattr(models.Hypothesis, key) == value)


    # Apply sorting
    if sort_by:
        sort_column = getattr(models.Hypothesis, sort_by, None)
        if sort_column:
            query = query.order_by(desc(sort_column) if sort_order == "desc" else asc(sort_column))

    paginated_result = paginate(query, page, per_page)

    return {
        "total_pages": paginated_result.pages,
        "total_items": paginated_result.total,
        "current_page": page,
        "items": paginated_result.items,
    }

def get_hypothesis_by_id(
        db: Session,
        hypothesis_id: str
) -> Optional[models.Hypothesis]:
    """
    Fetches a hypothesis by their id.
    """
    return db.query(models.Hypothesis).filter(
        models.Hypothesis.id == hypothesis_id
    ).first()

def get_validation_results_by_hypothesis_id(db: Session, hypothesis_id: str):
    """
    Retrieve all validation results for a given hypothesis.
    """
    return db.query(models.ValidationResult).filter(
        models.ValidationResult.hypothesis_id == hypothesis_id
    ).all()
