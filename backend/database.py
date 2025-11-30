import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

DB_URL = os.getenv("DB_URL", "sqlite:///./recsys.db")
connect_args = {"check_same_thread": False} if DB_URL.startswith("sqlite") else {}

engine = create_engine(DB_URL, echo=False, future=True, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass

# ✅ 正确：FastAPI 期望带 yield 的依赖；不要返回内部函数
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
