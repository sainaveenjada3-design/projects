"""Request models (what the frontend sends to the API)."""

from pydantic import BaseModel


class AskRequest(BaseModel):
    question: str
