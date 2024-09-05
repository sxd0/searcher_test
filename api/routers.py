import csv
from datetime import datetime
import io
from fastapi import APIRouter, Depends, File, UploadFile, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session
from api.database import get_db, engine, Base
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