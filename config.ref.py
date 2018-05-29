import os


class Configuration(object):
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://your_mysql_username:your_mysql_password@mysql_hostname/mysql_db_name"
    SECRET_KEY = "your_secret_key"

    ### Flask-security 
    SECURITY_PASSWORD_SALT = "your_security_password_salt"
    SECURITY_PASSWORD_HASH = "sha512_crypt"

    MAIL_USERNAME="your_email@gmail.com",
    MAIL_PASSWORD="your_email_password"
