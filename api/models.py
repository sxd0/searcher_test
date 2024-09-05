from sqlalchemy import Column, Integer, String, TIMESTAMP, ARRAY
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    rubrics = Column(ARRAY(String), nullable=False)
    text = Column(String, nullable=False)
    created_date = Column(TIMESTAMP, nullable=False, default=datetime.datetime.utcnow)
