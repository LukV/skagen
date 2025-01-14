from typing import List
from fastapi import APIRouter, BackgroundTasks, HTTPException, Depends, status
from sqlalchemy.orm import Session
from crud import hypothesises as crud_hypothesises
from schemas import hypothesises as hypothesis_schemas
from db.database import get_db
from db import models
from core.auth import get_current_user
from core.utils import is_admin_or_entity_owner
from pipeline.orchestrator import start_validation_pipeline

router = APIRouter()

@router.post("/", response_model=hypothesis_schemas.HypothesisResponse)
def create_hypothesis(
    hypothesis: hypothesis_schemas.HypothesisCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
    ):
    """Create a new hypothesis in the database."""
    created_hypothesis = crud_hypothesises.create_hypothesis(db, hypothesis, current_user)
    return created_hypothesis

@router.get("/", response_model=List[hypothesis_schemas.HypothesisResponse])
def get_all_hypothesises(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Retrieve a list of all hypotheses, or only the user's hypotheses if not an admin."""
    hypothesises = crud_hypothesises.get_all_hypothesises(db, current_user)
    return [hypothesis_schemas.HypothesisResponse(**hypothesis.__dict__) \
             for hypothesis in hypothesises]

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
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    _current_user: models.User = Depends(
        is_admin_or_entity_owner(
            crud_hypothesises.get_hypothesis_by_id,
            entity_name="Hypothesis",
            entity_id_param="hypothesis_id",
        )
    )
):
    """Update an existing hypothesis's details."""
    updated_hypothesis, is_content_updated = crud_hypothesises.update_hypothesis(
        db, hypothesis_id, hypothesis_update
    )

    if is_content_updated:
        hypothesis_id = str(updated_hypothesis.id)
        background_tasks.add_task(start_validation_pipeline, hypothesis_id, db)

    return updated_hypothesis

@router.delete("/{hypothesis_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_hypothesis(
    hypothesis_id: str,
    db: Session = Depends(get_db),
    _current_user: models.User = Depends(
        is_admin_or_entity_owner(
            crud_hypothesises.get_hypothesis_by_id,
            entity_name="Hypothesis",
            entity_id_param="hypothesis_id",
        )
    )
):
    """Delete an existing hypothesis from the database. This is a hard delete."""
    crud_hypothesises.delete_hypothesis(db, hypothesis_id)

@router.post("/{hypothesis_id}/validations", status_code=status.HTTP_202_ACCEPTED)
def run_validation_pipeline(
    hypothesis_id: str,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    _current_user: models.User = Depends(get_current_user)
):
    """
    Trigger the validation pipeline for a specific hypothesis.
    """
    # Check if the hypothesis exists
    hypothesis = crud_hypothesises.get_hypothesis_by_id(db, hypothesis_id)
    if not hypothesis:
        raise HTTPException(status_code=404, detail="Hypothesis not found")

    # Trigger the validation pipeline in the background
    background_tasks.add_task(start_validation_pipeline, hypothesis_id, db)

    return {
        "message": "Validation pipeline started for hypothesis.", 
        "hypothesis_id": hypothesis_id
    }

@router.get("/{hypothesis_id}/validations", \
            response_model=List[hypothesis_schemas.ValidationResultResponse])
def get_validation_results(
    hypothesis_id: str,
    db: Session = Depends(get_db),
    _current_user: models.User = Depends(get_current_user)
):
    """
    Retrieve all validation results for a given hypothesis.
    """
    # Fetch the hypothesis to ensure it exists
    hypothesis = crud_hypothesises.get_hypothesis_by_id(db, hypothesis_id)
    if not hypothesis:
        raise HTTPException(status_code=404, detail="Hypothesis not found")

    # Get all validation results for the hypothesis
    validation_results = crud_hypothesises. \
        get_validation_results_by_hypothesis_id(db, hypothesis_id)

    # Convert validation results to response models
    return [
        hypothesis_schemas.ValidationResultResponse(**validation_result.__dict__)
        for validation_result in validation_results
    ]
