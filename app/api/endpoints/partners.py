from fastapi import APIRouter, Depends, File, HTTPException
from sqlalchemy.orm import Session

from typing import Annotated
from app.api.deps import get_db
from app.crud import crud_partner
from app import schemas
from app.services import partner


router = APIRouter()

@router.get("/")
def root():
    return {"message": "Hello World"}

@router.get("/partners/", response_model=list[schemas.Partner] | None)
def read_partners(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    partners = crud_partner.get_partners(db, skip=skip, limit=limit)
    return partners

@router.post("/partners/", response_model=schemas.Partner)
def create_partner(partner: schemas.Partner, db: Session = Depends(get_db)):
    db_partner = crud_partner.find_partner_by_cnpj_or_email(db, cnpj=partner.cnpj, email=partner.email)
    if db_partner:
        raise HTTPException(status_code=409, detail="Partner already registered")
    return crud_partner.create_partner(db=db, partner=partner)

@router.post("/bulk-partners/", response_model=list[schemas.Partner])
def create_partners(file: Annotated[bytes, File()], db: Session = Depends(get_db)):
    partners = partner.from_csv(file, db)
    return partners