"""FastAPI application entry point and route registration."""

import time
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from prometheus_fastapi_instrumentator import Instrumentator
from sqlalchemy.exc import OperationalError

from . import models
from .database import engine
from .routes import comments, posts, users

app = FastAPI(title="Blog API")

ROOT_DIR = Path(__file__).resolve().parents[2]
FRONTEND_DIR = ROOT_DIR / "frontend"
app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR)), name="static")

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


@app.get("/", include_in_schema=False)
def root():
    """Serve the frontend app at the root URL."""
    index_path = FRONTEND_DIR / "index.html"
    return FileResponse(index_path)


app.include_router(users.router)
app.include_router(posts.router)
app.include_router(comments.router)


@app.get("/{full_path:path}", include_in_schema=False)
def serve_frontend(full_path: str):
    """Serve frontend static files or return index.html for client-side routing."""
    # Let API routes (registered above) take precedence; this runs for unmatched paths.
    candidate = FRONTEND_DIR / full_path
    if candidate.exists() and candidate.is_file():
        return FileResponse(candidate)
    return FileResponse(FRONTEND_DIR / "index.html")
