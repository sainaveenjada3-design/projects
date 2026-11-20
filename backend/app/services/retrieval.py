"""Step 1 of answering a question: find relevant documents in the Knowledge Base."""

import logging
from dataclasses import dataclass, field

from app.aws_clients import bedrock_agent_runtime_client
from app.config import KNOWLEDGE_BASE_ID, RETRIEVAL_RESULT_COUNT

logger = logging.getLogger(__name__)

NO_SOURCE = "Source not available"


@dataclass
class RetrievalResult:
    """What came back from the Knowledge Base."""

    count: int = 0                                   # chunks returned by AWS
    context_parts: list[str] = field(default_factory=list)  # text for the prompt
    sources: list[str] = field(default_factory=list)        # unique S3 URIs


def retrieve_documents(question: str) -> RetrievalResult:
    logger.info("Retrieving documentation for: %s", question)

    response = bedrock_agent_runtime_client.retrieve(
        knowledgeBaseId=KNOWLEDGE_BASE_ID,
        retrievalQuery={"text": question},
        retrievalConfiguration={
            "vectorSearchConfiguration": {
                "numberOfResults": RETRIEVAL_RESULT_COUNT
            }
        },
    )

    items = response.get("retrievalResults", [])
    result = RetrievalResult(count=len(items))

    logger.info("Retrieved document count: %s", result.count)

    for number, item in enumerate(items, start=1):
        content = item.get("content", {}).get("text", "")
        score = item.get("score")
        source = (
            item.get("location", {})
            .get("s3Location", {})
            .get("uri", NO_SOURCE)
        )

        logger.info("Document %s | score=%s | source=%s", number, score, source)
        logger.debug("Content: %s", content[:1000])

        if content.strip():
            result.context_parts.append(
                f"DOCUMENT {number}\n\nSOURCE: {source}\n\nCONTENT:\n{content}"
            )

        if source != NO_SOURCE and source not in result.sources:
            result.sources.append(source)

    return result
