from fastapi import Depends
from sqlalchemy.orm import Session
from app import models


def clean(db: Session):
    db.query(models.Partner).delete()
    db.commit()
