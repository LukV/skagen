from sqlalchemy import JSON, Column, ForeignKey, String, DateTime
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

class Hypothesis(Base):
    __tablename__ = "hypothesises"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"), index=True, nullable=False)
    user = relationship("User", back_populates="hypotheses")
    content = Column(String, nullable=False)
    status = Column(String, default='Pending')
    extracted_topics = Column(JSON, nullable=False, default=[])
    extracted_terms = Column(JSON, nullable=False, default=[])
    extracted_entities = Column(JSON, nullable=False, default=[])
    query_type = Column(String, nullable=False, default='unknown')
    date_created = Column(DateTime(timezone=True), server_default=func.now()) # pylint: disable=E1102
    date_updated = Column(DateTime(timezone=True), onupdate=func.now()) # pylint: disable=E1102
