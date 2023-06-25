# from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, EmailStr

class BasePartner(BaseModel):
    email: EmailStr
    cnpj: str
    company_name: str
    trading_name: str
    telephone: str
    zip_code: str

class PartnerCreate(BasePartner):
    pass


class PartnerUpdate(BasePartner):
    updated_at: datetime


class PartnerInDB(BasePartner):
    id: int = None
    created_at: datetime = None
    updated_at: datetime = None

    class Config:
        orm_mode = True


class Partner(PartnerInDB):
    pass