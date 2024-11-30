import time
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError

# Connect to the PostgreSQL database running in Docker
DATABASE_URL = "postgresql://catalog_user:catalog_pass@quest-catalog-db:5432/quest-catalog-db"

def wait_for_db():
    while True:
        try:
            temp_engine = create_engine(DATABASE_URL)
            connection = temp_engine.connect()
            connection.close()
            print("Quest Catalog Database is ready!")
            break
        except OperationalError:
            print("Database not ready, retrying in 2 seconds...")
            time.sleep(2)

wait_for_db()

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependency for database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()