from sqlalchemy import Column, Integer, String, JSON, TIMESTAMP, func
from services.db import Base

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    raw_mood = Column(String, nullable=False)
    normalized_mood = Column(String, nullable=False)
    style = Column(String, nullable=False)
    country = Column(String, nullable=False)
    language = Column(String, nullable=False)
    image_url = Column(String, nullable=True)
    captions = Column(JSON, nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now())   