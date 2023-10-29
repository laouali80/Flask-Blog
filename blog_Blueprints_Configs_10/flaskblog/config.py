import os

class Config:
    # to secure forms from across attacks, modifiying cokies
    SECRET_KEY = os.environ.get('SECRET_KEY')

    # configure the database
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')

    # configure the email sent
    MAIL_SERVER = 'smtp.googlemail.com' 
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('EMAIL_USER') 
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS') 