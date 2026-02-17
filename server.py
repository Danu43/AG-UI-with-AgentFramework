import os
from fastapi.middleware.cors import CORSMiddleware
from typing import Annotated
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import Field
from agent_framework import Agent, tool
from agent_framework.azure import AzureOpenAIChatClient
from agent_framework_ag_ui import add_agent_framework_fastapi_endpoint




load_dotenv()

# Validate required environment variables
required_vars = [
    "AZURE_OPENAI_ENDPOINT",
    "AZURE_OPENAI_CHAT_DEPLOYMENT_NAME",
    "AZURE_OPENAI_API_KEY",
    "AZURE_OPENAI_VERSION"
]

for var in required_vars:
    if not os.getenv(var):
        raise RuntimeError(f"Missing required environment variable: {var}")

# Create Azure OpenAI chat client
chat_client = AzureOpenAIChatClient(
    endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    deployment_name=os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version=os.getenv("AZURE_OPENAI_VERSION"),
)

# Define tool
@tool
def get_order_status(
    order_id: Annotated[str, Field(description="Order ID like ORD-001")]
) -> dict:
    """Returns order status, tracking number, and ETA."""

    orders = {
        "ORD-001": {"status": "shipped", "tracking": "1Z999AA1", "eta": "Jan 25, 2026"},
        "ORD-002": {"status": "processing", "tracking": None, "eta": "Jan 23, 2026"},
        "ORD-003": {"status": "delivered", "tracking": "1Z999AA3", "eta": "Delivered Jan 20"},
    }

    return orders.get(order_id, {"status": "not_found", "message": "Order not found"})


# Create agent (1.0 style)
agent = Agent(
    name="CustomerSupportAgent",
    instructions="""
You are a helpful customer support assistant.

When a user provides an order ID like ORD-001,
you MUST call the get_order_status tool.

Never guess order details.
After calling the tool, present results clearly and friendly.
""",
    client=chat_client,
    tools=[get_order_status],
)

# FastAPI app
app = FastAPI(
    title="AG-UI Customer Support (1.0 SDK)",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Mount AG-UI endpoint
add_agent_framework_fastapi_endpoint(app, agent, path="/chat")

if __name__ == "__main__":
    import uvicorn
    print("Starting AG-UI server at http://localhost:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)
