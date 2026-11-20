"""
API NEXUS - application entry point.

Creates the FastAPI app, serves the frontend files and registers the routes.
Run it with:  python run.py   (from the backend folder)
"""

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.config import FRONTEND_DIR
from app.logging_config import setup_logging
from app.routes import api, pages

setup_logging()

app = FastAPI(
    title="API NEXUS - API Documentation Assistant",
    description=(
        "Ask questions about uploaded Python API documentation "
        "using Amazon Bedrock Knowledge Base."
    ),
    version="1.0.0",
)

# Frontend CSS / JS / images are available under /static/...
app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

app.include_router(pages.router)
app.include_router(api.router)
