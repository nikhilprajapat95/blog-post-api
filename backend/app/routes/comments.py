"""API routes for managing comments on posts."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db
from ..dependencies import get_authenticated_user

router = APIRouter(tags=["comments"])


@router.get("/posts/{post_id}/comments", response_model=list[schemas.CommentRead])
def read_comments(post_id: int, db: Session = Depends(get_db)):
    """Get comments for a specific post."""
    comments = db.query(models.Comment).filter(models.Comment.post_id == post_id).all()
    return comments


@router.post(
    "/posts/{post_id}/comments",
    response_model=schemas.CommentRead,
    status_code=status.HTTP_201_CREATED,
)
def create_comment(
    post_id: int,
    comment_in: schemas.CommentCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_authenticated_user),
):
    """Create a comment on a post. Requires authentication."""
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    comment = models.Comment(
        text=comment_in.text,
        post_id=post_id,
        author_id=current_user.id,
    )
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment
