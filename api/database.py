from fastapi import HTTPException
from sqlalchemy import Column, Index, Integer, String, Text, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

from api.models import Document, Base

DATABASE_URL = "postgresql://doc_user:123456@localhost:5432/documents_db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    Base.metadata.create_all(bind=engine)





def search_documents(db: Session, query: str):
    try:
        results = db.query(Document).filter(Document.text.ilike(f"%{query}%")).limit(20).all()
        return results
    except Exception as e:
        print(f"Error during search: {e}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    init_db()