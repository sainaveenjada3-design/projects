"""Start the API NEXUS server:  python run.py"""

import uvicorn

from app import config

if __name__ == "__main__":
    print("\n======================================")
    print("       API NEXUS APPLICATION")
    print("======================================")
    print("AWS REGION      :", config.AWS_REGION or "Not configured")
    print("S3 BUCKET       :", config.S3_BUCKET_NAME or "Not configured")
    print("KNOWLEDGE BASE  :", config.KNOWLEDGE_BASE_ID or "Not configured")
    print("MODEL CONFIGURED:", bool(config.BEDROCK_MODEL_ARN))
    print("FRONTEND        :", config.INDEX_FILE)
    print("======================================\n")

    uvicorn.run(
        "app.main:app",
        host=config.SERVER_HOST,
        port=config.SERVER_PORT,
        reload=False,
    )
