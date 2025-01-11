from datetime import datetime
from typing import List, Optional
from enum import Enum
from pydantic import BaseModel, ConfigDict, Field

class HypothesisStatus(str, Enum):
    PENDING = "Pending"
    PROCESSING = "Processing"
    COMPLETED = "Completed"
    SKIPPED = "Skipped"
    FAILED = "Failed"

class QueryType(str, Enum):
    UNKNOWN = "unknown"
    RESEARCH_BASED = "research-based"
    FACTUAL = "factual"
    ABSTRACT = "abstract"

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
    extracted_entities: Optional[List[str]] = None
    query_type: Optional[QueryType] = None

class HypothesisResponse(BaseModel):
    id: str
    content: str
    user_id: str
    status: HypothesisStatus
    extracted_topics: List[str] = Field(default_factory=list)
    extracted_terms: List[str] = Field(default_factory=list)
    extracted_entities: List[str] = Field(default_factory=list)
    query_type: QueryType
    date_created: datetime
    date_updated: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)

class ValidationResultResponse(BaseModel):
    id: str
    hypothesis_id: str
    classification: Optional[str]
    motivation: Optional[str]
    sources: List[dict] = Field(default_factory=list)
    date_created: datetime
    date_updated: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)
