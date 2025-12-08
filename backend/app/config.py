import os
from urllib.parse import quote_plus
from dotenv import load_dotenv


load_dotenv()


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-change-me")

    MYSQL_USER = os.getenv("MYSQL_USER")
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
    MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
    MYSQL_PORT = int(os.getenv("MYSQL_PORT", "3306"))
    MYSQL_DB = os.getenv("MYSQL_DB", "cloudlabs")

  
    if MYSQL_USER and MYSQL_PASSWORD and MYSQL_HOST:
        _encoded_pwd = quote_plus(MYSQL_PASSWORD or "")
        SQLALCHEMY_DATABASE_URI = os.getenv(
            "SQLALCHEMY_DATABASE_URI",
            f"mysql+pymysql://{MYSQL_USER}:{_encoded_pwd}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}",
        )
    else:
        SQLALCHEMY_DATABASE_URI = "sqlite:///cloudlabs.db"

    SQLALCHEMY_TRACK_MODIFICATIONS = False
