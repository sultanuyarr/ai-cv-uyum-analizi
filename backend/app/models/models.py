from typing import Optional
from datetime import datetime
from sqlmodel import Field, SQLModel, JSON
from sqlalchemy import Column
import uuid

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    hashed_password: str
    full_name: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

class Analysis(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    job_title: str
    job_description_text: str
    cv_text: str # Extracted text only
    overall_score: Optional[int] = None
    status: str = Field(default="PENDING") # PENDING, COMPLETED, FAILED
    result_json: Optional[str] = None # JSON string
    created_at: datetime = Field(default_factory=datetime.utcnow)
