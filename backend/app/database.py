"""Database setup using SQLAlchemy.

This file creates the engine, session factory, and declarative base.
It also provides a dependency function for FastAPI routes.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from .config import DATABASE_URL

# connect_args is only needed for SQLite.
connect_args = {}
engine_args = {}
if DATABASE_URL.startswith("sqlite"):
    connect_args["check_same_thread"] = False
    engine_args["poolclass"] = StaticPool

# Create the SQLAlchemy engine for all database operations.
engine = create_engine(DATABASE_URL, connect_args=connect_args, **engine_args)

# Create a configured "SessionLocal" class.
# Each request should use its own database session instance.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for our SQLAlchemy models.
Base = declarative_base()


def get_db():
    """Yield a database session for dependency injection."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
