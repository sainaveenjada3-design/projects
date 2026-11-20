"""Routes that serve the frontend page and the logo image."""

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

from app.config import INDEX_FILE, LOGO_CANDIDATES

router = APIRouter()


# All of these URLs open the same single-page site.
# The script in the page scrolls to the right section.
@router.get("/")
@router.get("/home")
@router.get("/ui")
@router.get("/technology")
@router.get("/workflow")
def index_page():
    if not INDEX_FILE.is_file():
        raise HTTPException(status_code=404, detail="Frontend index.html not found")

    return FileResponse(INDEX_FILE)


@router.get("/logo")
def logo():
    for logo_file in LOGO_CANDIDATES:
        if logo_file.is_file():
            return FileResponse(logo_file, media_type="image/png")

    raise HTTPException(
        status_code=404,
        detail="iSpace logo image not found in frontend/images.",
    )
