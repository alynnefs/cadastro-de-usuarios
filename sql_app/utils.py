from email_validator import validate_email, EmailNotValidError
from validate_docbr import CPF, PIS

def is_cpf_valid(user_cpf: str):
    cpf = CPF()
    return cpf.validate(user_cpf)

def is_pis_valid(user_pis: str):
    pis = PIS()
    return pis.validate(user_pis)

def is_email_valid(user_email: str):
    try:
        valid = validate_email(user_email)
        user_email = valid.email
        return True
    except EmailNotValidError as e:
        print(str(e))
        return False
