import os

class Config:

    SECRET_KEY = 'erass'
    # SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://erastus:Angular2020@localhost/last1'
    UPLOADED_PHOTOS_DEST = 'app/static/photos'

    #  email configurations
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME= "erastuskariuki15@gmail.com"
    MAIL_PASSWORD = "e1r2a3s4"
    SENDER_EMAIL = 'erastuskariuki15@gmail.com'


class ProdConfig(Config):

    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")


class DevConfig(Config):

    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    # SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://erastus:Angular2020@localhost/last1'
    DEBUG = True


config_options = {
'development':DevConfig,
'production':ProdConfig
} 

