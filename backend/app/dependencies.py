"""Shared dependencies for FastAPI route handling."""

from fastapi import Depends
from sqlalchemy.orm import Session

from .auth import get_current_user
from .database import get_db
from .models import User


def get_db_session() -> Session:
    """Provide a SQLAlchemy database session to route handlers."""
    return Depends(get_db)


def get_authenticated_user(current_user: User = Depends(get_current_user)) -> User:
    """Provide the current authenticated user to route handlers."""
    return current_user
