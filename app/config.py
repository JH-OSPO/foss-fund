import os

BASE_DIR = os.path.dirname(os.path.abspath(__name__))

db_type=os.environ.get("DB_TYPE")
db_name=os.environ.get("DB_NAME")
db_host=os.environ.get("DB_HOST")
db_port=os.environ.get("DB_PORT", 3306)
db_user=os.environ.get("DB_USER")
db_pass=os.environ.get("DB_PASS")

def build_connect_string():
    if db_type == "mysql":
        print("Choosing mysql to connect")
        s = f"mysql+pymysql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
        print(s)
        return s
    else:
        print("Falling back to sqlite")
        return f"sqlite:///{os.path.join(BASE_DIR, 'database.db')}"
        
class Config:
    DEBUG = True

    SECRET_KEY="kE5RVcD36LclaM2UHKX3X1dnAMlBgteZ"
    SQLALCHEMY_DATABASE_URI = build_connect_string()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_ADMIN_KEY = os.getenv("SECRET_ADMIN_KEY")
