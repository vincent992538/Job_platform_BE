from enum import Enum
from datetime import date, datetime
from typing import get_args, List, Literal
from typing_extensions import Self
import json

from django.core.exceptions import ValidationError
from ninja import Schema, FilterSchema, Field
from pydantic import model_validator


JOB_SORT_COLUMNS = Literal[
    'posting_date', '-posting_date',
    'expiration_date', '-expiration_date'
]
STR_JOB_SORT_COLUMNS = ", ".join(
    get_args(JOB_SORT_COLUMNS)
)


class JobStatus(str, Enum):
    active = "active"
    expired = "expired"
    scheduled = "scheduled"


class JobBase(Schema):
    title: str = Field(..., max_length=255)
    description: str
    location: str = Field(..., max_length=255)
    company_name: str = Field(..., max_length=255)
    salary_range: str = Field(..., examples=["10k-100k"], max_length=100)
    posting_date: date
    expiration_date: date
    required_skills: List[str]


class JobIn(JobBase):
    @model_validator(mode="after")
    def check_date_range(self) -> Self:
        if self.posting_date >= self.expiration_date:
            raise ValidationError(
                "Expriration date must be after posting date."
            )
        return self


class JobOut(JobBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        json_encoders = {
            list: lambda v: json.dumps(v)  # Ensure list is serialized to string
        }


class JobUpdate(Schema):
    title: str | None = Field(None, max_length=255)
    description: str | None = None
    location: str | None = Field(None, max_length=255)
    salary_range: str | None = Field(
        None, examples=["10k-100k"], max_length=100
    )
    posting_date: date | None = None
    expiration_date: date | None = None
    required_skills: List[str] | None = None

    @model_validator(mode="after")
    def check_date_range(self) -> Self:
        if self.posting_date and self.expiration_date:
            if self.posting_date >= self.expiration_date:
                raise ValidationError(
                    "Expriration date must be after posting date."
                )
        return self


class JobFilterSchema(FilterSchema):
    query: str | None = Field(
        None,
        q=[
            "title__icontains",
            "description__icontains",
            "company_name__icontains"
        ]
    )
    location: str | None = Field(None, q="location__icontains")
    salary_range: str | None = Field(None, q="salary_range__icontains")
    required_skill: str | None = Field(None, q="required_skills__icontains")

    status: JobStatus | None = None
    ordering: JOB_SORT_COLUMNS | None = Field(
        None,
        description=f"Order by {STR_JOB_SORT_COLUMNS}"
    )
