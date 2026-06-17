"""Application configuration values for the FastAPI project."""

import os

# The database connection URL for SQLite.
# Local development uses a file-based SQLite database.
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./blog.db",
)

# Secret key used to sign JWT tokens.
# In production, override this with a strong secret from the environment.
SECRET_KEY = os.getenv("SECRET_KEY", "change-this-secret-key")

# JWT algorithm used for token encoding.
ALGORITHM = "HS256"

# Access token expiration window.
ACCESS_TOKEN_EXPIRE_MINUTES = 60
