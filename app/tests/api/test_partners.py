from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.main import app

from app.tests.utils.partner import create_random_partner
from app.tests.utils.db import clean

api_str = "http://localhost:8000"

def test_read_partners(client: TestClient, db: Session):
    clean(db)

    partner = create_random_partner(db)
    response = client.get(f"{api_str}/partners/")
    content = response.json()

    assert response.status_code == 200
    assert content[0]["email"] == partner.email
    assert content[0]["cnpj"] == partner.cnpj
    assert content[0]["company_name"] == partner.company_name
    assert content[0]["trading_name"] == partner.trading_name
    assert content[0]["telephone"] == partner.telephone
    assert content[0]["zip_code"] == partner.zip_code
    assert content[0]["city"] == partner.city
    assert content[0]["state"] == partner.state

def test_read_partners_empty(client: TestClient, db: Session):
    clean(db)

    response = client.get(f"{api_str}/partners/")
    content = response.json()

    assert response.status_code == 200
    assert content == []

def test_create_partners_with_file_without_errors(client: TestClient, db: Session):
    clean(db)

    file_str = "CNPJ,Razão Social,Nome Fantasia,Telefone,Email, CEP\n12.473.742/0001-13,Sol Forte,Sol Forte LTDA,(11) 98207-9903,atendimento@solforte.com,04127-000\n19.478.819/0001-97,Sol da Manhã,Sol da Manhã LTDA,(21) 98207-9902,atendimento@soldamanha.com,04127-000\n19.478.812/0001-90,Sol Energia,Sol Energia LTDA,(71) 98207-1902,atendimento@solenergia.com,04127-000\n16.470.954/0001-06,Sol Eterno,Sol Eterno LTDA,(21) 98207-9901,atendimento@soleterno.com,04127-000"

    response = client.post("/bulk-partners", files={"file": file_str})
    content = response.json()
    sorted_content = sorted(content, key=lambda x: x['id'])

    assert response.status_code == 200
    assert len(content) == 4
    assert sorted_content[0]["cnpj"] == "12.473.742/0001-13"
    assert sorted_content[1]["cnpj"] == "19.478.819/0001-97"
    assert sorted_content[2]["cnpj"] == "19.478.812/0001-90"
    assert sorted_content[3]["cnpj"] == "16.470.954/0001-06"

def test_create_partners_with_error(client: TestClient, db: Session):
    clean(db)

    file_str = "CNPJ,Razão Social,Nome Fantasia,Telefone,Email, CEP\n12.473.742/0001-13,Sol Forte,Sol Forte LTDA,(11) 98207-9903,wrongmail,04127-000"
    response = client.post("/bulk-partners", files={"file": file_str})

    assert response.status_code == 400
    