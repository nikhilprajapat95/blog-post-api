"""Pydantic schemas for request and response validation."""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, EmailStr


class Token(BaseModel):
    """Schema for the JWT access token response."""

    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Schema for token payload data."""

    username: Optional[str] = None


class UserBase(BaseModel):
    """Shared user fields."""

    username: str
    email: EmailStr


class UserCreate(UserBase):
    """Fields required when a new user registers."""

    password: str


class UserRead(UserBase):
    """Fields returned when a user is read from the API."""

    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class PostBase(BaseModel):
    """Shared fields for a post."""

    title: str
    content: str


class PostCreate(PostBase):
    """Fields required to create a new post."""

    pass


class PostRead(PostBase):
    """Fields returned when a post is read from the API."""

    id: int
    author_id: int
    created_at: datetime

    class Config:
        orm_mode = True


class CommentBase(BaseModel):
    """Shared fields for a comment."""

    text: str


class CommentCreate(CommentBase):
    """Fields required to create a comment."""

    pass


class CommentRead(CommentBase):
    """Fields returned when a comment is read from the API."""

    id: int
    post_id: int
    author_id: int
    created_at: datetime

    class Config:
        orm_mode = True
