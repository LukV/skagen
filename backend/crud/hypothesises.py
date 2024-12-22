from typing import List, Optional
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
        content=hypothesis.content,
        extracted_topics=[],
        extracted_terms=[]
    )
    db.add(db_hypothesis)
    db.commit()
    db.refresh(db_hypothesis)
    return db_hypothesis

def update_hypothesis(
    db: Session,
    hypothesis_id: str,
    hypothesis_update: hypothesis_schemas.HypothesisUpdate
) -> models.Hypothesis:
    """
    Updates an existing hypothesis's details in the database.
    """
    db_hypothesis = db.query(models.Hypothesis).filter(models.Hypothesis.id == hypothesis_id).first()
    if not db_hypothesis:
        raise HTTPException(status_code=404, detail="Hypothesis not found.")
    update_data = hypothesis_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_hypothesis, key, value)
    db.commit()
    db.refresh(db_hypothesis)
    return db_hypothesis

def delete_hypothesis(db: Session, hypothesis_id: str) -> Optional[models.Hypothesis]:
    """
    Deletes an existing hypothesis from the database.

    Args:
        db (Session): The database session.
        hypothesis_id (int): The ID of the hypothesis to delete.

    Returns:
        hypothesis or None: The deleted hypothesis instance or None if not found.
    """
    db_hypothesis = db.query(models.Hypothesis).filter(models.Hypothesis.id == hypothesis_id).first()
    if db_hypothesis:
        db.delete(db_hypothesis)
        db.commit()
    return db_hypothesis

def get_all_hypothesises(db: Session, current_user: models.User) -> List[models.Hypothesis]:
    """
    Retrieves all hypothesises from the database.
    """
    if current_user.role == 'admin':
        return db.query(models.Hypothesis).all()
    else:
        return db.query(models.Hypothesis).filter(models.Hypothesis.user_id == current_user.id).all()

def get_hypothesis_by_id(db: Session, hypothesis_id: str) -> Optional[models.Hypothesis]:
    """
    Fetches a hypothesis by their id.
    """
    return db.query(models.Hypothesis).filter(models.Hypothesis.id == hypothesis_id).first()