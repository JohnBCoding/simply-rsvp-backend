import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    CSRF_ENABLED = True
    SQLALCHEMY_DATABASE_URI = os.environ["DATABASE_URL"]
    GMAIL_USER = os.environ["GMAIL_USER"]
    GMAIL_PASS = os.environ["GMAIL_PASS"]
