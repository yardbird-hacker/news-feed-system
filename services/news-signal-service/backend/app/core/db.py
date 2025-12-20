from sqlmodel import Session, create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

# 기존 engine (SQLModel에서도 SQLAlchemy engine 사용)
engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URI,
    pool_pre_ping=True,
    pool_recycle=3600,
)

# ✅ 추가: Kafka consumer / repository 용 SessionLocal
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

# 기존 FastAPI / SQLModel에서 사용하는 helper (있다면 유지)
def get_session() -> Session:
    with Session(engine) as session:
        yield session
