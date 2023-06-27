from sqlalchemy.orm import Session
from app import models, schemas
from fastapi.encoders import jsonable_encoder
from typing import Dict, Any


def get_partners(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Partner).offset(skip).limit(limit).all()

def find_partner_by_cnpj_or_email(db: Session, cnpj: str, email: str):
    return db.query(models.Partner).filter((models.Partner.cnpj == cnpj) | (models.Partner.email == email)).first()

def create_partner(db: Session, partner: schemas.PartnerCreate):
    obj_in_data = jsonable_encoder(partner)
    db_partner = models.Partner(**obj_in_data)
    db.add(db_partner)
    db.commit()
    db.refresh(db_partner)
    return db_partner

def update_partner(db: Session, db_obj: schemas.PartnerInDB, obj_in: schemas.PartnerUpdate | Dict[str, Any]):
    obj_data = jsonable_encoder(db_obj)
    if isinstance(obj_in, dict):
        update_data = obj_in
    else:
        update_data = obj_in.dict(exclude_unset=True)
    for field in obj_data:
        if field in update_data:
            setattr(db_obj, field, update_data[field])
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj
