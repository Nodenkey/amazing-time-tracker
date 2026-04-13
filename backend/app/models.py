from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, Field, field_validator


class TimeEntryBase(BaseModel):
    date: date = Field(..., description="Entry date in ISO format (YYYY-MM-DD)")
    person_name: str = Field(..., min_length=1, description="Name of the person logging time")
    activity: str = Field(..., min_length=1, description="Description of the activity")
    duration_minutes: int = Field(..., gt=0, description="Duration of the activity in minutes")
    notes: Optional[str] = Field(None, description="Optional free-form notes")

    @field_validator("person_name", "activity")
    @classmethod
    def non_blank_strings(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("must not be blank")
        return v.strip()


class TimeEntryCreate(TimeEntryBase):
    pass


class TimeEntryUpdate(BaseModel):
    date: Optional[date] = None
    person_name: Optional[str] = Field(None, min_length=1)
    activity: Optional[str] = Field(None, min_length=1)
    duration_minutes: Optional[int] = Field(None, gt=0)
    notes: Optional[str] = None

    @field_validator("person_name", "activity")
    @classmethod
    def non_blank_optional_strings(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        if not v.strip():
            raise ValueError("must not be blank")
        return v.strip()


class TimeEntry(TimeEntryBase):
    id: str
    created_at: datetime

    class Config:
        from_attributes = True
