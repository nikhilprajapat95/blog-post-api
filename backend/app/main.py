"""FastAPI application entry point and route registration."""

import time

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator
from sqlalchemy.exc import OperationalError

from . import models
from .database import engine
from .routes import comments, posts, users

app = FastAPI(title="Blog API")

# Set up Prometheus metrics instrumentation.
Instrumentator().instrument(app).expose(app)

# Enable CORS so the frontend can call this API from a different origin.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000", "http://localhost"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def wait_for_database(retries: int = 10, delay: float = 3.0) -> None:
    """Wait for the database to become available before applying schema migrations."""
    for attempt in range(1, retries + 1):
        try:
            with engine.connect():
                return
        except OperationalError:
            if attempt == retries:
                raise
            time.sleep(delay)


# Wait for the configured database to be ready before creating tables.
wait_for_database()
models.Base.metadata.create_all(bind=engine)


@app.get("/health")
def health_check():
    """Kubernetes and load balancers use this endpoint to verify the app is running."""
    return {"status": "ok"}


@app.get("/readiness")
def readiness_check():
    """Readiness tells Kubernetes the app is ready to receive traffic."""
    return {"status": "ready"}


@app.get("/")
def root():
    """Root endpoint for health checks and default browser access."""
    return {"status": "ok", "message": "Blog API is running"}


app.include_router(users.router)
app.include_router(posts.router)
app.include_router(comments.router)
