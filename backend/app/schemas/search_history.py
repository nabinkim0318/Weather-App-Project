from datetime import datetime

from pydantic import BaseModel, Field


class SearchHistoryItem(BaseModel):
    query: str = Field(..., description="The user's search input")
    searched_at: datetime = Field(..., description="Timestamp of the search")

    class Config:
        from_attributes = True


class AddSearchHistoryRequest(BaseModel):
    query: str = Field(..., description="The query string to add to search history")
