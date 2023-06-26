import copy, csv, re
from sqlalchemy.orm import Session
from app.crud import crud_partner
from datetime import datetime
from app.schemas import BasePartner

def upsert_from_csv(file: bytes, db: Session): 
    csv_data = file.decode('utf-8') 

    validated_csv = validate_csv(csv_data)
    if validated_csv["errors"]:
        file_path = '../assets/output.csv'
        write_errors(validated_csv["rows"], file_path)

        return file_path

    partners = []
    for row in csv.DictReader(csv_data.splitlines()):
        state_and_city = get_state_and_city(row[' CEP'])
        partner_obj = format_partner(row, state_and_city)
        partner = crud_partner.find_partner_by_cnpj_or_email(db, cnpj=partner_obj.cnpj, email=partner_obj.email)
        if partner:
            partner = crud_partner.update_partner(db, db_obj=partner, obj_in={**partner_obj.dict(),"updated_at": datetime.now()})
        else:
            partner = crud_partner.create_partner(db, partner=partner_obj)
        partners.append(partner)

    return partners

def validate_csv(csv_data: str):
    reader = csv.DictReader(csv_data.splitlines()) 

    rows = []
    all_errors = []

    for row in reader:
        errors = []
        for fieldname, value in row.items():
            if not value:
                errors.append(f"{fieldname} is empty.")

            if fieldname == "CNPJ" and value and not validate_cnpj(value):
                errors.append(f"Invalid CNPJ: {value}")

            if fieldname == "Telefone" and value and not validate_telefone(value):
                errors.append(f"Invalid telefone: {value}")

            if fieldname == "CEP" and value and not validate_cep(value):
                errors.append(f"Invalid CEP: {value}")

            if fieldname == "Email" and value and not validate_email(value):
                errors.append(f"Invalid email: {value}")

        row["Erros"] = ", ".join(errors)
        all_errors.append(errors)

        rows.append(row)
   
    return {"rows": rows, "errors": sum(all_errors, [])}

def write_errors(data, file_path):
    fieldnames = data[0].keys()

    with open(file_path, 'w', newline='') as file:
        csv_writer = csv.DictWriter(file, fieldnames=fieldnames)
        csv_writer.writeheader()

        return csv_writer.writerows(data)

def validate_cnpj(cnpj):
    # CNPJ pattern: xx.xxx.xxx/xxxx-xx
    pattern = r"^(\d{2}.?\d{3}.?\d{3}\/?\d{4}\-?\d{2})$"
    return re.fullmatch(pattern, cnpj) is not None

def validate_telefone(telefone):
    # Telefone pattern: (xx) xxxxx-xxxx
    pattern = r"\(\d{2}\) \d{5}-\d{4}"
    return re.fullmatch(pattern, telefone) is not None

def validate_cep(cep):
    # CEP pattern: xxxxx-xxx
    pattern = r"(^\d{5})\-?(\d{3}$)"
    return re.fullmatch(pattern, cep) is not None

def validate_email(email):
    # Email pattern validation using a simple regex pattern
    pattern = r"[^@ \t\r\n]+@[^@ \t\r\n]+\.[^@ \t\r\n]+"
    return re.fullmatch(pattern, email) is not None

def format_partner(row: list[str], state_and_city: dict):
    cnpj = row['CNPJ']
    company_name = row['Razão Social']
    trading_name = row['Nome Fantasia']
    telephone = row['Telefone']
    email = row['Email']
    zip_code = row[' CEP']

    return BasePartner(
        cnpj = cnpj, 
        email = email, 
        company_name = company_name,
        trading_name = trading_name, 
        telephone = telephone, 
        zip_code = zip_code,
        city=state_and_city["city"],
        state=state_and_city["state"]
    )

def get_state_and_city(cep: str):
    try:
        address_obj = brazilcep.get_address_from_cep(cep)
        return {"city": address_obj["city"], "state": address_obj["uf"]}
    except:
        return {"city": None, "state": None}