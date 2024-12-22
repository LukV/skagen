from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field, EmailStr, model_validator
from enum import Enum

class HypothesisStatus(str, Enum):
    PENDING = "Pending"
    PROCESSING = "Processing"
    COMPLETED = "Completed"
    FAILED = "Failed"
    
class HypothesisCreate(BaseModel):
    content: str = Field(
        ...,
        min_length=3,
        max_length=500,
        description="The text by the user that describes the hypothesis."
    )

class HypothesisUpdate(BaseModel):
    content: Optional[str] = Field(
        None,
        min_length=3,
        max_length=500,
        description="The updated hypothesis text."
    )
    status: Optional[HypothesisStatus] = None
    extracted_topics: Optional[List[str]] = None
    extracted_terms: Optional[List[str]] = None

class HypothesisResponse(BaseModel):
    id: str
    content: str
    user_id: str
    status: HypothesisStatus
    extracted_topics: List[str] = Field(default_factory=list)
    extracted_terms: List[str] = Field(default_factory=list)
    date_created: datetime
    date_updated: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)