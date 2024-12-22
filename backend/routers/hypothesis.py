from typing import List
from fastapi import APIRouter, BackgroundTasks, File, HTTPException, Depends, UploadFile, status
from sqlalchemy.orm import Session
from crud import hypothesises as crud_hypothesises
from schemas import hypothesises as hypothesis_schemas
from db.database import get_db
from db import models
from core.auth import get_current_user
from core.utils import is_admin_or_entity_owner

router = APIRouter()

@router.post("/", response_model=hypothesis_schemas.HypothesisResponse)
def create_hypothesis(
    hypothesis: hypothesis_schemas.HypothesisCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
    ):
    """Create a new hypothesis in the database."""
    return crud_hypothesises.create_hypothesis(db, hypothesis, current_user)

@router.get("/", response_model=List[hypothesis_schemas.HypothesisResponse])
def get_all_hypothesises(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Retrieve a list of all hypotheses, or only the user's hypotheses if not an admin."""
    hypothesises = crud_hypothesises.get_all_hypothesises(db, current_user)
    return [hypothesis_schemas.HypothesisResponse(**hypothesis.__dict__) for hypothesis in hypothesises]

@router.get("/{hypothesis_id}", response_model=hypothesis_schemas.HypothesisResponse)
def get_hypothesis(
    hypothesis_id: str,
    db: Session = Depends(get_db)
):
    """Retrieve a hypothesis's details."""
    hypothesis = crud_hypothesises.get_hypothesis_by_id(db, hypothesis_id)
    if not hypothesis:
        raise HTTPException(status_code=404, detail="hypothesis not found")

    return hypothesis_schemas.HypothesisResponse(**hypothesis.__dict__)

@router.put("/{hypothesis_id}", response_model=hypothesis_schemas.HypothesisResponse)
def update_hypothesis(
    hypothesis_id: str,
    hypothesis_update: hypothesis_schemas.HypothesisUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(
        is_admin_or_entity_owner(
            crud_hypothesises.get_hypothesis_by_id,
            entity_name="Hypothesis",
            entity_id_param="hypothesis_id",
        )
    ) # pylint: disable=W0613
):
    """Update an existing hypothesis's details."""
    return crud_hypothesises.update_hypothesis(db, hypothesis_id, hypothesis_update)

@router.delete("/{hypothesis_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_hypothesis(
    hypothesis_id: str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(
        is_admin_or_entity_owner(
            crud_hypothesises.get_hypothesis_by_id,
            entity_name="Hypothesis",
            entity_id_param="hypothesis_id",
        )
    ) # pylint: disable=W0613
):
    """Delete an existing hypothesis from the database. This is a hard delete."""
    crud_hypothesises.delete_hypothesis(db, hypothesis_id)
