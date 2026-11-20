"""API routes: GET /health and POST /ask."""

import logging

from botocore.exceptions import BotoCoreError, ClientError
from fastapi import APIRouter, HTTPException

from app import config
from app.schemas import AskRequest
from app.services.generation import NOT_FOUND_MESSAGE, generate_answer
from app.services.retrieval import retrieve_documents

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/health")
def health():
    return {
        "status": "healthy",
        "application": "API NEXUS",
        "aws_region": config.AWS_REGION,
        "knowledge_base_configured": bool(config.KNOWLEDGE_BASE_ID),
        "model_configured": bool(config.BEDROCK_MODEL_ARN),
    }


def check_configuration() -> None:
    """Stop early with a clear message if .env is incomplete."""
    missing = config.missing_settings()

    if missing:
        raise HTTPException(
            status_code=500,
            detail=f"{missing[0]} is missing in .env.",
        )


# This is a normal `def` (not `async def`) on purpose: boto3 is blocking,
# so FastAPI runs it in a worker thread and other requests keep working.
@router.post("/ask")
def ask_question(request: AskRequest):
    check_configuration()

    question = request.question.strip()

    if not question:
        raise HTTPException(status_code=400, detail="Please enter a question.")

    logger.info("User question received: %s", question)

    try:
        # Step 1: find relevant documents
        retrieval = retrieve_documents(question)

        if not retrieval.context_parts:
            logger.warning("No relevant documentation retrieved.")
            return {
                "status": "no_results",
                "question": question,
                "answer": NOT_FOUND_MESSAGE,
                "sources": [],
                "retrieved_count": retrieval.count,
            }

        # Step 2: let the model write the answer
        answer = generate_answer(question, retrieval.context_parts)

        logger.info("Answer generated successfully.")

        return {
            "status": "success",
            "question": question,
            "answer": answer or NOT_FOUND_MESSAGE,
            "sources": retrieval.sources,
            "retrieved_count": retrieval.count,
        }

    except ClientError as error:
        details = error.response.get("Error", {})
        logger.exception("AWS ClientError occurred.")
        raise HTTPException(
            status_code=500,
            detail={
                "error_code": details.get("Code", "Unknown"),
                "message": details.get("Message", str(error)),
            },
        )

    except BotoCoreError as error:
        logger.exception("AWS connection error.")
        raise HTTPException(status_code=500, detail=str(error))

    except Exception as error:
        logger.exception("Unexpected error occurred.")
        raise HTTPException(status_code=500, detail=str(error))
