import csv
from datetime import datetime
import io
from fastapi import APIRouter, Depends, File, UploadFile, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.orm import Session
from api.database import get_db, engine, Base, search_documents
from api.models import Document
from sqlalchemy.exc import IntegrityError

router = APIRouter() 



@router.post("/import-csv/")
async def import_csv(file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        contents = await file.read()
        csv_file = io.StringIO(contents.decode('utf-8'))
        reader = csv.reader(csv_file)
        
        next(reader)
        
        for row in reader:
            if len(row) != 4:
                continue
            
            rubrics = row[0]
            text = row[1]
            created_date_str = row[2]
            try:
                created_date = datetime.strptime(created_date_str, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                continue
            
            document = Document(rubrics=rubrics, text=text, created_date=created_date)
            db.add(document)
        
        db.commit()
        return {"status": "success"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error processing file: {str(e)}")

@router.get("/test-db/")
async def test_db(db: Session = Depends(get_db)):
    try:
        query = text("SELECT 1")
        result = db.execute(query).scalar()
        if result == 1:
            return {"status": "success"}
        else:
            return {"status": "failed"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database test failed: {str(e)}")
    
@router.get("/search/")
def search(query: str, db: Session = Depends(get_db)):
    results = search_documents(db, query)
    return results

@router.delete("/documents/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_document(document_id: int, db: Session = Depends(get_db)):
    document = db.query(Document).filter(Document.id == document_id).first()
    
    if document is None:
        raise HTTPException(status_code=404, detail="Document not found")
    
    db.delete(document)
    db.commit()
    
    return {"detail": "Document successfully deleted"}

@router.get("/documents/{document_id}")
def get_document(document_id: int, db: Session = Depends(get_db)):
    document = db.query(Document).filter(Document.id == document_id).first()
    if document is None:
        raise HTTPException(status_code=404, detail="Document not found")
    return document