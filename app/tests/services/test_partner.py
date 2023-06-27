from fastapi import BackgroundTasks
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.tests.utils.db import clean
from app.services import partner

def test_create_from_function_upsert_from_csv(client: TestClient, db: Session, bg_task: BackgroundTasks = BackgroundTasks()):
    clean(db)
    
    file_str = "CNPJ,Razão Social,Nome Fantasia,Telefone,Email, CEP\n12.473.742/0001-13,Sol Forte,Sol Forte LTDA,(11) 98207-9903,atendimento@solforte.com,04127-000\n19.478.819/0001-97,Sol da Manhã,Sol da Manhã LTDA,(21) 98207-9902,atendimento@soldamanha.com,04127-000"
    partners = partner.upsert_from_csv(file_str.encode(), db=db, bg_task=bg_task)
    sorted_partners = sorted(partners, key=lambda x: x.id)

    assert len(partners) == 2
    assert sorted_partners[0].cnpj == "12.473.742/0001-13"
    assert sorted_partners[1].cnpj == "19.478.819/0001-97"

def test_update_from_function_upsert_from_csv(client: TestClient, db: Session, bg_task: BackgroundTasks = BackgroundTasks()):
    clean(db)
    
    file_str = "CNPJ,Razão Social,Nome Fantasia,Telefone,Email, CEP\n12.473.742/0001-13,Sol Forte,Sol Forte LTDA,(11) 98207-9903,atendimento@solforte.com,04127-000\n19.478.819/0001-97,Sol da Manhã,Sol da Manhã LTDA,(21) 98207-9902,atendimento@soldamanha.com,04127-000"
    # First step create the partners
    partner.upsert_from_csv(file_str.encode(), db=db, bg_task=bg_task)
    # Second step update the partners
    partners = partner.upsert_from_csv(file_str.encode(), db=db, bg_task=bg_task)

    assert len(partners) == 2
    assert partners[0].updated_at != None
    assert partners[1].updated_at != None

def test_validate_csv_with_wrong_email(client: TestClient, db: Session):
    clean(db)
    
    file_str = "CNPJ,Razão Social,Nome Fantasia,Telefone,Email, CEP\n12.473.742/0001-13,Sol Forte,Sol Forte LTDA,(11) 98207-9903,@solforte.com,04127-000\n19.478.819/0001-97,Sol da Manhã,Sol da Manhã LTDA,(21) 98207-9902,wrongemail,04127-000"
    partners = partner.validate_csv(file_str)

    assert partners["errors"] == ['Invalid email: @solforte.com', 'Invalid email: wrongemail']

def test_validate_csv_with_wrong_cnpj(client: TestClient, db: Session):
    clean(db)
    
    file_str = "CNPJ,Razão Social,Nome Fantasia,Telefone,Email, CEP\n530.774.460-90,Sol Forte,Sol Forte LTDA,(11) 98207-9903,atendimento@solforte.com,04127-000\n19.478.819/0001-97,Sol da Manhã,Sol da Manhã LTDA,(21) 98207-9902,atendimento@soldamanha.com,04127-000"
    partners = partner.validate_csv(file_str)

    assert partners["errors"] == ['Invalid CNPJ: 530.774.460-90']

def test_validate_csv_with_wrong_telephone(client: TestClient, db: Session):
    clean(db)
    
    file_str = "CNPJ,Razão Social,Nome Fantasia,Telefone,Email, CEP\n12.473.742/0001-13,Sol Forte,Sol Forte LTDA,132,atendimento@solforte.com,04127-000\n19.478.819/0001-97,Sol da Manhã,Sol da Manhã LTDA,(21) 222,atendimento@soldamanha.com,04127-000"
    partners = partner.validate_csv(file_str)

    assert partners["errors"] == ['Invalid telefone: 132', 'Invalid telefone: (21) 222']

def test_validate_csv_with_wrong_zipcode(client: TestClient, db: Session):
    clean(db)
    
    file_str = "CNPJ,Razão Social,Nome Fantasia,Telefone,Email, CEP\n12.473.742/0001-13,Sol Forte,Sol Forte LTDA,(11) 98207-9903,atendimento@solforte.com,04127\n19.478.819/0001-97,Sol da Manhã,Sol da Manhã LTDA,(21) 98207-9902,atendimento@soldamanha.com,200"
    partners = partner.validate_csv(file_str)

    assert partners["errors"] == ['Invalid CEP: 04127', 'Invalid CEP: 200']

def test_validate_csv_with_missing_data(client: TestClient, db: Session):
    clean(db)
    
    file_str = "CNPJ,Razão Social,Nome Fantasia,Telefone,Email, CEP\n,Sol Forte,,,atendimento@solforte.com,04127-000\n19.478.819/0001-97,Sol da Manhã,Sol da Manhã LTDA,(21) 98207-9902,atendimento@soldamanha.com,"
    partners = partner.validate_csv(file_str)

    assert partners["errors"] == ['CNPJ is empty.', 'Nome Fantasia is empty.', 'Telefone is empty.', ' CEP is empty.']
    