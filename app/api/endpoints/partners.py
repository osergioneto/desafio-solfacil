from fastapi import APIRouter, Depends, File, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from typing import Annotated
from app.api.deps import get_db
from app.crud import crud_partner
from app import schemas
from app.services import partner


router = APIRouter()

@router.get("/partners/", response_model=list[schemas.Partner] | None)
def read_partners(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    partners = crud_partner.get_partners(db, skip=skip, limit=limit)
    return partners


@router.post("/bulk-partners/", response_model=list[schemas.Partner] | None)
def create_partners(file: Annotated[bytes, File()], db: Session = Depends(get_db)):
    parterns_or_file = partner.upsert_from_csv(file, db)
    if isinstance(parterns_or_file, list):
        return parterns_or_file
    
    return FileResponse(parterns_or_file, status_code=400)