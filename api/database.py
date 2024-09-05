from sqlalchemy import Column, Index, Integer, String, Text, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

DATABASE_URL = "postgresql://doc_user:123456@localhost:5432/documents_db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    Base.metadata.create_all(bind=engine)


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), index=True)
    content = Column(Text, index=True)

    # Добавляем индекс для быстрого поиска по тексту
    __table_args__ = (
        Index('ix_documents_content', 'content', postgresql_using='gin'),
    )

def search_documents(db: Session, query: str):
    results = db.query(Document).filter(Document.content.ilike(f'%{query}%')).limit(20).all()
    return results

if __name__ == "__main__":
    init_db()