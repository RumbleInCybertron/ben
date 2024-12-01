import time
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import logging
from sqlalchemy.exc import OperationalError
import traceback

DATABASE_URL = "postgresql://processing_user:processing_pass@quest-processing-db:5432/quest-processing-db"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def wait_for_db():
    while True:
        try:
            temp_engine = create_engine(DATABASE_URL)
            connection = temp_engine.connect()
            connection.close()
            print("Quest Catalog Database is ready!")
            break
        except OperationalError as e:
            print("Database not ready, retrying in 2 seconds...")
            print(f"Error details: {e}")
            print(traceback.format_exc())  # Print the full traceback for debugging
            time.sleep(2)

wait_for_db()

try:
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base = declarative_base()
except Exception as e:
    logger.error(f"Database connection failed: {e}")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
