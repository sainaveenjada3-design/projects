"""
AWS (boto3) clients.

The clients are created once, when the app starts, and only if
AWS_REGION is configured. Credentials are picked up by boto3 from the
.env file, `aws configure`, or an IAM role.
"""

import boto3

from app.config import AWS_REGION

# Used to search the Knowledge Base
bedrock_agent_runtime_client = None

# Used to call the foundation model
bedrock_runtime_client = None

if AWS_REGION:
    bedrock_agent_runtime_client = boto3.client(
        "bedrock-agent-runtime", region_name=AWS_REGION
    )
    bedrock_runtime_client = boto3.client(
        "bedrock-runtime", region_name=AWS_REGION
    )
