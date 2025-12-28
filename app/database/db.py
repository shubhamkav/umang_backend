from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

load_dotenv()

# DATABASE_URL = (
#     f"mysql+pymysql://{os.getenv('DB_USER')}:"
#     f"{os.getenv('DB_PASSWORD')}@"
#     f"{os.getenv('DB_HOST')}/"
#     f"{os.getenv('DB_NAME')}"
# )
DB_PASSWORD= "LeRevlWUw4vTEbRoDXz1QSqmeKd1GY63"
DB_HOST="dpg-d57mssbuibrs73a8t4v0-a.singapore-postgres.render.com"
DB_PORT="5432"
DB_NAME="student_registration_yc20"
DB_USER="student_registration_yc20_user"
# postgresql://student_registration_yc20_user:LeRevlWUw4vTEbRoDXz1QSqmeKd1GY63@dpg-d57mssbuibrs73a8t4v0-a.singapore-postgres.render.com/student_registration_yc20
DATABASE_URL = (
    f"postgresql+psycopg2://{DB_USER}:"
    f"{DB_PASSWORD}@"
    f"{DB_HOST}:"
    f"{DB_PORT}/"
    f"{DB_NAME}"
)

engine = create_engine(DATABASE_URL, echo=False)

SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
