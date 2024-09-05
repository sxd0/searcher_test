from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from sqlalchemy import text
from .database import get_db
from .models import Document
import csv
from io import StringIO

router = APIRouter()

@router.post("/import")
async def import_csv(file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        file_content = await file.read()
        file_content = file_content.decode('utf-8')
        csv_reader = csv.DictReader(StringIO(file_content))
        
        for row in csv_reader:
            document = Document(
                rubrics=row['rubrics'].split(','),
                text=row['text'],
                created_date=row['created_date']
            )
            db.add(document)
        
        db.commit()
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/test-db")
async def test_db(db: Session = Depends(get_db)):
    try:
        result = db.execute(text("SELECT 1")).fetchone()
        return {"status": "success", "result": result[0]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
