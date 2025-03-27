import re

def validate_email(email):
    if not email:
        return False
    
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def validate_password(password, min_length=8, require_uppercase=True, 
                     require_lowercase=True, require_digit=True, 
                     require_special=True):
    if not password:
        return False, "Le mot de passe ne peut pas être vide"
    
    if len(password) < min_length:
        return False, f"Le mot de passe doit contenir au moins {min_length} caractères"
    
    if require_uppercase and not re.search(r'[A-Z]', password):
        return False, "Le mot de passe doit contenir au moins une lettre majuscule"
    
    if require_lowercase and not re.search(r'[a-z]', password):
        return False, "Le mot de passe doit contenir au moins une lettre minuscule"
    
    if require_digit and not re.search(r'\d', password):
        return False, "Le mot de passe doit contenir au moins un chiffre"
    
    if require_special and not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False, "Le mot de passe doit contenir au moins un caractère spécial"
    
    return True, None

def validate_credit_card(card_number):
    if not card_number or not card_number.isdigit():
        return False
    
    digits = [int(d) for d in card_number][::-1]
    
    total = 0
    for i, digit in enumerate(digits):
        if i % 2 == 1:
            digit *= 2
            if digit > 9:
                digit -= 9
        total += digit
    
    return total % 10 == 0

def validate_phone_number(phone):
    if not phone:
        return False
    
    phone = re.sub(r'\D', '', phone)
    
    if len(phone) < 10 or len(phone) > 15:
        return False
    
    return True

def validate_postal_code(postal_code, country='FR'):
    if not postal_code:
        return False
    
    postal_code = postal_code.strip()
    
    if country == 'FR':
        return bool(re.match(r'^\d{5}$', postal_code))
    elif country == 'US':
        return bool(re.match(r'^\d{5}(-\d{4})?$', postal_code))
    elif country == 'CA':
        return bool(re.match(r'^[A-Za-z]\d[A-Za-z] \d[A-Za-z]\d$', postal_code))
    elif country == 'GB':
        return bool(re.match(r'^[A-Za-z]{1,2}\d[A-Za-z\d]? \d[A-Za-z]{2}$', postal_code))
    else:
        return bool(re.match(r'^[A-Za-z0-9- ]{3,10}$', postal_code))