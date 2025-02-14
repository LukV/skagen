from sqlalchemy import JSON, Column, ForeignKey, String, DateTime, UniqueConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=True)
    icon = Column(String, nullable=True)
    role = Column(String, default='user')
    date_created = Column(DateTime(timezone=True), server_default=func.now()) # pylint: disable=E1102
    hypotheses = relationship("Hypothesis", back_populates="user")
    feedbacks = relationship("Feedback", back_populates="user")

class Hypothesis(Base):
    __tablename__ = "hypothesises"

    id = Column(String, primary_key=True, index=True)

    user_id = Column(String, ForeignKey("users.id"), index=True, nullable=False)
    user = relationship("User", back_populates="hypotheses")

    parent_id = Column(String, ForeignKey("hypothesises.id"), nullable=True, default=None)
    parent = relationship("Hypothesis", remote_side=[id], backref="children")

    content = Column(String, nullable=False)
    status = Column(String, default='Pending')
    extracted_topics = Column(JSON, nullable=False, default=[])
    extracted_terms = Column(JSON, nullable=False, default=[])
    extracted_entities = Column(JSON, nullable=True, default=[])
    query_type = Column(String, nullable=False, default='unknown')
    date_created = Column(DateTime(timezone=True), server_default=func.now()) # pylint: disable=E1102
    date_updated = Column(DateTime(timezone=True), onupdate=func.now()) # pylint: disable=E1102

    validation_results = relationship("ValidationResult", back_populates="hypothesis")
    feedbacks = relationship("Feedback", back_populates="hypothesis")

class ValidationResult(Base):
    __tablename__ = "validation_results"

    id = Column(String, primary_key=True, index=True)

    hypothesis_id = Column(String, ForeignKey("hypothesises.id"), index=True, nullable=False)
    hypothesis = relationship("Hypothesis", back_populates="validation_results")

    classification = Column(String, nullable=True)
    motivation = Column(String, nullable=True)
    sources = Column(JSON, nullable=True, default=[])
    date_created = Column(DateTime(timezone=True), server_default=func.now()) # pylint: disable=E1102
    date_updated = Column(DateTime(timezone=True), onupdate=func.now()) # pylint: disable=E1102

class AcademicWork(Base):
    __tablename__ = "academic_works"

    id = Column(String, primary_key=True, index=True)
    abstract = Column(String, nullable=True)
    apa_citation = Column(String, nullable=False)
    authors = Column(JSON, nullable=True, default=[])
    authors_formatted = Column(String, nullable=True)
    core_id = Column(String, nullable=False)
    links = Column(JSON, nullable=True, default=[])
    full_text = Column(String, nullable=True)
    published_date = Column(String, nullable=True)
    publisher = Column(JSON, nullable=True)
    title = Column(String, nullable=False)
    year_published = Column(String, nullable=True)
    llm_summary = Column(String, nullable=True)
    llm_keywords = Column(String, nullable=True)
    llm_phrase = Column(String, nullable=True)
    llm_extended_summary = Column(String, nullable=True)
    date_created = Column(DateTime(timezone=True), server_default=func.now()) # pylint: disable=E1102
    date_updated = Column(DateTime(timezone=True), onupdate=func.now()) # pylint: disable=E1102

    __table_args__ = (
        UniqueConstraint('core_id', name='uq_academicwork_core_id'),
    )

class Feedback(Base):
    __tablename__ = "hypothesis_feedback"

    id = Column(String, primary_key=True, index=True)

    user_id = Column(String, ForeignKey("users.id"), index=True, nullable=False)
    user = relationship("User", back_populates="feedbacks")

    hypothesis_id = Column(String, ForeignKey("hypothesises.id"), index=True, nullable=False)
    hypothesis = relationship("Hypothesis", back_populates="feedbacks")

    action = Column(String, nullable=False)
    comment = Column(String, nullable=True)
    date_created = Column(DateTime(timezone=True), server_default=func.now()) # pylint: disable=E1102
