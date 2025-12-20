from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.constants import DATABASE_URL

# Добавляем retry логику для Docker
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    echo=False,
    connect_args={
        "connect_timeout": 10
    }
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class TaskDB(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, nullable=False)
    quadrant = Column(Integer, nullable=False)
    done = Column(Boolean, default=False)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Функция для проверки и создания таблиц
def init_database():
    """Инициализирует базу данных при запуске"""
    try:
        Base.metadata.create_all(bind=engine)
        print("База данных инициализирована")
    except Exception as e:
        print(f"Ошибка при инициализации БД: {e}")
