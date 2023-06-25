import csv
from sqlalchemy.orm import Session
from app.crud import crud_partner

def from_csv(file: bytes, db: Session): 
    csv_data = file.decode() 
    reader = csv.reader(csv_data.splitlines()) 
    partners = []

    next(reader)

    for row in reader:
        cnpj = row[0]
        company_name = row[1]
        trading_name = row[2]
        telephone = row[3]
        email = row[4]
        zip_code = row[5]

        partner = crud_partner.find_partner_by_cnpj_or_email(db, cnpj=cnpj, email=email)
        # print(partner.__dict__)
        if partner:
            print("Encontrou partner")
            partner = crud_partner.update_partner(db, db_obj=partner, obj_in={
                "cnpj": cnpj, 
                "email": email, 
                "company_name": company_name,
                "trading_name": trading_name, 
                "telephone": telephone, 
                "zip_code": zip_code
            })
            partners.append(partner)
            print("Atualizou partner")
            print("partners", partners)
        else:
            print("Não achou")
            partner = crud_partner.create_partner(db, partner={
                "cnpj": cnpj, 
                "email": email, 
                "company_name": company_name,
                "trading_name": trading_name, 
                "telephone": telephone, 
                "zip_code": zip_code
            })
            print("Criou partner", partner)
            partners.append(partner)
            print("partners", partners)
        # print(row)
    print("partners", partners)
    return partners