import csv
from sqlalchemy.orm import Session
from .models import Document
from .database import get_db, Base, engine
from fastapi import Depends, FastAPI


Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post("/import-csv/")
def import_csv(db: Session = Depends(get_db)):
    with open('/data/posts.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            document = Document(
                id=row['id'],
                rubrics=row['rubrics'].split(','),
                text=row['text'],
                created_date=row['created_date']
            )
            db.add(document)
        db.commit()
    return {"status": "success"}



