from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field

class Author(BaseModel):
    name: str = Field(..., description="The full name of the author.")

class AcademicWorkCreate(BaseModel):
    abstract: Optional[str] = Field(
        None, description="The abstract of the academic work."
    )
    authors: Optional[List[Author]] = Field(
        None, description="A list of authors for the academic work, each with a name field."
    )
    core_id: str = Field(
        ..., description="The unique core ID associated with the academic work."
    )
    full_text: Optional[str] = Field(
        None, description="The full text content of the academic work."
    )
    published_date: Optional[str] = Field(
        None, description="The publication date of the academic work in ISO format."
    )
    publisher: Optional[str] = Field(
        None, description="The publisher's information as a string."
    )
    title: str = Field(
        ..., description="The title of the academic work."
    )
    year_published: Optional[str] = Field(
        None, description="The year the academic work was published."
    )

class AcademicWorkResponse(BaseModel):
    id: str = Field(
        ..., description="A unique public identifier for the academic work."
    )
    abstract: Optional[str] = Field(
        None, description="The abstract of the academic work."
    )
    apa_citation: str = Field(
        ..., description="The APA citation format for the academic work."
    )
    authors: Optional[List[Author]] = Field(
        None, description="A list of authors for the academic work, each with a name field."
    )
    authors_formatted: Optional[str] = Field(
        None, description="Formatted string of authors' names for display."
    )
    core_id: str = Field(
        ..., description="The unique core ID associated with the academic work."
    )
    full_text: Optional[str] = Field(
        None, description="The full text content of the academic work."
    )
    published_date: Optional[str] = Field(
        None, description="The publication date of the academic work in ISO format."
    )
    publisher: Optional[str] = Field(
        None, description="The publisher's information as a string."
    )
    title: str = Field(
        ..., description="The title of the academic work."
    )
    year_published: Optional[str] = Field(
        None, description="The year the academic work was published."
    )
    date_created: datetime = Field(
        ..., description="The timestamp when the academic work was created."
    )

    model_config = ConfigDict(from_attributes=True)
