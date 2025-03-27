import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'une-cle-secrete-difficile-a-deviner'
    DEBUG = False
    TESTING = False
    

class DevelopmentConfig(Config):
    DEBUG = True
   

class TestingConfig(Config):
    TESTING = True
    

class ProductionConfig(Config):
   
    SECRET_KEY = os.environ.get('SECRET_KEY')
    