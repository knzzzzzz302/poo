import re
from src.models.user import RegularUser, PremiumUser, BusinessUser

class UserService:
    
    def __init__(self):
        self.users = {}
        self.email_to_user = {}
        self.username_to_user = {}
    
    def validate_email(self, email):
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    def validate_password(self, password):
        if len(password) < 8:
            return False
        
        if not re.search(r'[A-Z]', password):
            return False
        
        if not re.search(r'\d', password):
            return False
        
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            return False
        
        return True
    
    def register(self, username, email, password, user_type='regular', company_name=None):
        if not username or not email or not password:
            raise ValueError("Tous les champs sont obligatoires")
        
        if not self.validate_email(email):
            raise ValueError("Format d'email invalide")
        
        if not self.validate_password(password):
            raise ValueError("Le mot de passe n'est pas assez fort")
        
        if email in self.email_to_user:
            raise ValueError("Cette adresse email est déjà utilisée")
        
        if username in self.username_to_user:
            raise ValueError("Ce nom d'utilisateur est déjà utilisé")
        
        if user_type.lower() == 'premium':
            user = PremiumUser(username, email, password)
        elif user_type.lower() == 'business':
            if not company_name:
                raise ValueError("Le nom de l'entreprise est obligatoire pour les utilisateurs professionnels")
            user = BusinessUser(username, email, password, company_name)
        else:
            user = RegularUser(username, email, password)
        
        self.users[user.id] = user
        self.email_to_user[email] = user
        self.username_to_user[username] = user
        
        return user
    
    def authenticate(self, email, password):
        user = self.email_to_user.get(email)
        
        if user and user.verify_password(password):
            return user
        
        return None
    
    def get_user_by_id(self, user_id):
        return self.users.get(user_id)
    
    def get_user_by_email(self, email):
        return self.email_to_user.get(email)
    
    def get_user_by_username(self, username):
        return self.username_to_user.get(username)
    
    def update_user(self, user_id, username=None, email=None, password=None):
        user = self.get_user_by_id(user_id)
        
        if not user:
            return None
        
        if username and username != user.username:
            if username in self.username_to_user:
                raise ValueError("Ce nom d'utilisateur est déjà utilisé")
            
            del self.username_to_user[user.username]
            self.username_to_user[username] = user
            user.username = username
        
        if email and email != user.email:
            if not self.validate_email(email):
                raise ValueError("Format d'email invalide")
            
            if email in self.email_to_user:
                raise ValueError("Cette adresse email est déjà utilisée")
            
            del self.email_to_user[user.email]
            self.email_to_user[email] = user
            user.email = email
        
        if password:
            if not self.validate_password(password):
                raise ValueError("Le mot de passe n'est pas assez fort")
            
            user.password_hash = user._hash_password(password)
        
        return user
    
    def delete_user(self, user_id):
        user = self.get_user_by_id(user_id)
        
        if not user:
            return False
        
        del self.users[user_id]
        del self.email_to_user[user.email]
        del self.username_to_user[user.username]
        
        return True
    
    def get_all_users(self):
        return list(self.users.values())