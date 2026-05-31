from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Session
from typing import Generator
import os

# Connexion base de donnée
engine = create_engine(os.getenv('DATABASE_URL'), pool_size=10, echo=True)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

class Base(DeclarativeBase):
    pass

#Accès base de donnée
def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db        # FastAPI injecte la session dans la route
    finally:
        db.close()      # fermeture session