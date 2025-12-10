import os
import time
import logging
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, BigInteger, String, Integer, Boolean
import psycopg2
from psycopg2 import OperationalError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DB_HOST = os.environ.get('POSTGRES_HOST', 'postgres')
DB_NAME = os.environ.get('POSTGRES_DB', 'todo_app')
DB_USER = os.environ.get('POSTGRES_USER', 'postgres')
DB_PASSWORD = os.environ.get('POSTGRES_PASSWORD', 'secret')
DATABASE_URL = os.environ.get('DATABASE_URL', f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:5432/{DB_NAME}")


def wait_for_db(max_retries=10, retry_interval=2):
    for i in range(max_retries):
        try:
            conn = psycopg2.connect(
                host=DB_HOST,
                database=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD
            )
            conn.close()
            logger.info('База данных готова')
            return True
        except OperationalError as e:
            if i < max_retries - 1:
                logger.warning(f'База данных не готова, повторная попытка... ({i + 1}/{max_retries})')
                time.sleep(retry_interval)
            else:
                logger.error(f'Не удалось подключиться к базе данных: {e}')
                raise e
    return False


wait_for_db()

engine = create_engine(DATABASE_URL)

try:
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
        logger.info('SQLAlchemy успешно подключился к БД')
except Exception as e:
    logger.error(f'Ошибка подключения SQLAlchemy: {e}')
    raise

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class TaskModel(Base):
    __tablename__ = "tasks"

    id = Column(BigInteger, primary_key=True)
    text = Column(String, nullable=False)
    quadrant = Column(Integer, nullable=False)
    done = Column(Boolean, default=False)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
