from typing import List, Optional, Tuple
from fastapi import HTTPException
from sqlalchemy.orm import Session
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
        parent_id='None',
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

def get_all_hypothesises(db: Session, current_user: models.User) -> List[models.Hypothesis]:
    """
    Retrieves all hypotheses from the database.

    If the current user is an admin, retrieves all hypotheses.
    Otherwise, retrieves only the hypotheses created by the user.
    """
    if current_user.role == 'admin':   # pylint: disable=E1136
        return db.query(models.Hypothesis).all()

    return db.query(models.Hypothesis) \
        .filter(models.Hypothesis.user_id == current_user.id).all()

def get_hypothesis_by_id(db: Session, hypothesis_id: str) -> Optional[models.Hypothesis]:
    """
    Fetches a hypothesis by their id.
    """
    return db.query(models.Hypothesis).filter(models.Hypothesis.id == hypothesis_id).first()
