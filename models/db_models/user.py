from pydantic import BaseModel,Field
from typing import Any, Optional

class OutModel(BaseModel):
    status: str
    status_code: int
    comment: Optional[str]
    data: Any

class saveBookmark(BaseModel):
    bookmarkId: Optional[str]
    userId: Optional[str]
    basketId: Optional[str]

class buzzTableModel(BaseModel):
    buzzId:Optional[str]
    date: Optional[str]
    duration:Optional[str]
    logo:Optional[str]
    reason:Optional[str]
    target:Optional[str]
    ticker:Optional[str]
    vidhyaId:Optional[str]