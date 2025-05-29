# models/search_history.py
from sqlalchemy import Column, DateTime, Integer, String, func

from app.db.database import Base


class SearchHistory(Base):
    __tablename__ = "search_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    query = Column(String, nullable=False)
    searched_at = Column(DateTime, server_default=func.now(), nullable=False)
