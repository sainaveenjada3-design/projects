"""
Application settings.

Everything configurable lives here: folder paths and the values read
from the .env file. Other modules import from this file instead of
reading environment variables themselves.
"""

import os
from pathlib import Path

from dotenv import load_dotenv

# ---------------------------------------------------------
# Folder paths
# ---------------------------------------------------------

BACKEND_DIR = Path(__file__).resolve().parent.parent   # api-nexus/backend
PROJECT_DIR = BACKEND_DIR.parent                       # api-nexus
FRONTEND_DIR = PROJECT_DIR / "frontend"                # api-nexus/frontend

INDEX_FILE = FRONTEND_DIR / "index.html"
IMAGES_DIR = FRONTEND_DIR / "images"

# The first logo that exists is used by the /logo route
LOGO_CANDIDATES = [
    IMAGES_DIR / "ispace_logo_transparent.png",
    IMAGES_DIR / "ispace_logo.png",
]

# ---------------------------------------------------------
# Environment variables (backend/.env)
# ---------------------------------------------------------

load_dotenv(BACKEND_DIR / ".env", override=True)


def _get_env(name: str, default: str = "") -> str:
    return os.getenv(name, default).strip()


AWS_REGION = _get_env("AWS_REGION")
S3_BUCKET_NAME = _get_env("S3_BUCKET_NAME")
S3_PREFIX = _get_env("S3_PREFIX", "documents/")
KNOWLEDGE_BASE_ID = _get_env("KNOWLEDGE_BASE_ID")
DATA_SOURCE_ID = _get_env("DATA_SOURCE_ID")
BEDROCK_MODEL_ARN = _get_env("BEDROCK_MODEL_ARN")

# ---------------------------------------------------------
# Tuning values
# ---------------------------------------------------------

RETRIEVAL_RESULT_COUNT = 5     # how many chunks to fetch from the Knowledge Base
MODEL_MAX_TOKENS = 1500
MODEL_TEMPERATURE = 0.1
MODEL_TOP_P = 0.9

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 8001


def missing_settings() -> list[str]:
    """Return the names of required settings that are empty."""
    required = {
        "AWS_REGION": AWS_REGION,
        "KNOWLEDGE_BASE_ID": KNOWLEDGE_BASE_ID,
        "BEDROCK_MODEL_ARN": BEDROCK_MODEL_ARN,
    }
    return [name for name, value in required.items() if not value]
