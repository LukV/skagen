from sqlalchemy import Column, String, DateTime
from sqlalchemy.sql import func
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=True)
    icon = Column(String, nullable=True)
    date_created = Column(DateTime(timezone=True), server_default=func.now()) # pylint: disable=E1102
