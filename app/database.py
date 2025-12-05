from app.constants import DATABASE_URL, TABLE_NAME
from sqlalchemy import create_engine, Column, BigInteger, String, Integer, Boolean
from sqlalchemy.orm import sessionmaker, declarative_base


engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=True, bind=engine)
Base = declarative_base()


class TaskModel(Base):
    __tablename__ = TABLE_NAME
    id = Column(BigInteger, primary_key=True)
    text = Column(String, nullable=False)
    quadrant = Column(Integer, nullable=False)
    done = Column(Boolean, default=False)


def check_exist_table():
    from sqlalchemy import inspect
    inspector = inspect(engine)
    return inspector.has_table(TABLE_NAME)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
