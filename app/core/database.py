from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings


# Create the SQLAlchemy engine
def get_engine():
    return create_engine(
        settings.DATABSE_URL,
        connect_args={"check_same_thread": False}
    )


# Create SQLAlchemy session factory
def get_session_factory(engine):
    SessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine)

    return SessionLocal


# Create Tables or runs migrations
def init_db():
    engine = get_engine()
    return engine, get_session_factory(engine)


# FastAPI dependency to get DB session
def get_db():
    engine, SessionLocal = init_db()
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
