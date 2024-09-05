from sqlalchemy import Column, Index, Integer, String, TIMESTAMP, ARRAY, Text
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    rubrics = Column(ARRAY(String), nullable=False)
    text = Column(String, nullable=False)
    created_date = Column(TIMESTAMP, nullable=False, default=datetime.datetime.utcnow)
    title = Column(String(255), index=True)
    content = Column(Text, index=True)

    __table_args__ = (
        Index('ix_documents_content', 'content', postgresql_using='gin'),  # Индекс для быстрого поиска
    )