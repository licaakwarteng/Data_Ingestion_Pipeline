from sqlalchemy import Column, Integer, String, DateTime, Float
from datetime import datetime
from app.database import Base

class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    source_url = Column(String, nullable=False)
    filename = Column(String, nullable=True)
    status = Column(String, default="pending")
    file_size = Column(Float, nullable=True)
    bytes_processed = Column(Float, default=0)
    s3_key = Column(String, nullable=True)
    error_message = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.now)
    completed_at = Column(DateTime, nullable=True)