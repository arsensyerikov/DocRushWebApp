from pydantic import BaseModel, Field, EmailStr, field_validator
from typing import List, Optional
from datetime import datetime, timezone

class EventModel(BaseModel):
    name: str = Field(..., example="Annual Tech Conference")
    description: Optional[str] = Field(None, example="A conference about the latest in technology")
    start_datetime: datetime = Field(..., example="2024-12-25T09:00:00Z")
    emails: List[EmailStr] = Field(..., example=["example@example.com"])

    @field_validator('start_datetime', mode='before')
    def start_datetime_cannot_be_in_the_past(cls, v):
        # Ensure the datetime is aware and in UTC
        if isinstance(v, str):
            v = datetime.fromisoformat(v)
        if v.tzinfo is None:
            v = v.replace(tzinfo=timezone.utc)
        if v < datetime.now(timezone.utc):
            raise ValueError('start_datetime must be in the future')
        return v

    @field_validator('emails', mode='before')
    def validate_email_list(cls, v):
        # Validate each email in the list
        if not isinstance(v, list):
            raise ValueError("emails must be a list")
        for email in v:
            if not isinstance(email, EmailStr):
                raise ValueError(f"Invalid email: {email}")
        return v

    class Config:
        str_min_length = 1
        str_max_length = 255

# Test the model
try:
    event = EventModel(
        name="mercedes",
        start_datetime="2024-12-11T09:00:00Z",
        emails=["arsen@hjgfdc.com"]
    )
    print(event)
except Exception as e:
    print(f"Error: {e}")




























from fastapi import FastAPI, Query
from typing import Optional


app = FastAPI()


@app.get("/items/")
async def read_items(q: Optional[str] = Query(None, max_length=50)):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"filter": q})
    return results