from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.crud import crud_partner
from faker import Faker

fake = Faker(['pt-BR', 'en-US'])


def create_random_partner(db: Session):
    partner = schemas.PartnerCreate(
        email=fake.email(),
        cnpj=fake.cnpj(),
        company_name=fake.company(),
        trading_name=fake.company_suffix(),
        telephone=fake.phone_number(),
        zip_code=fake.postcode(),
        city=fake.city(),
        state=fake.estado_sigla()
    )
    return crud_partner.create_partner(db, partner=partner)