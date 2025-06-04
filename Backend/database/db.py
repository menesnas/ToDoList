from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
import os

# SQLAlchemy Base sınıfı
class Base(DeclarativeBase):
    pass

# Veritabanı için klasör oluşturma
os.makedirs("./database", exist_ok=True)

# SQLite veritabanı bağlantısı
SQLALCHEMY_DATABASE_URL = "sqlite:///./database/todos.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Bağımlılık - DB oturumu
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 