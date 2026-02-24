
EXCLUDE_TABLES = [
    "users", "threads", "steps", "elements", "feedbacks",
    "T_Reports", "T_Roles_Auth"
]

from pydantic import BaseModel
from typing import List, Dict, Any
# These imports handle environment configuration, API setup
import os
from fastapi.middleware.cors import CORSMiddleware
from typing import Annotated
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import Field


# This is where Microsoft Agent Framework and AG-UI are integrated.
# Agent defines agent behavior, tool registers callable tools, and add_agent_framework_fastapi_endpoint exposes an AG-UI compliant API

from agent_framework import Agent, tool
from agent_framework.azure import AzureOpenAIChatClient
from agent_framework_ag_ui import add_agent_framework_fastapi_endpoint


# Database Utilities 
from db import get_db_connection   
from db import get_all_tables_schema

# Here I dynamically extract the database schema and pass it to the agent so it understands table structures without hardcoding them
DB_SCHEMA = get_all_tables_schema(exclude_tables=EXCLUDE_TABLES) 
from sql_tools import execute_sql_query


load_dotenv()


# Environment Validation
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
# This initializes a secure Azure OpenAI chat client used by the agent for reasoning.
chat_client = AzureOpenAIChatClient(
    endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    deployment_name=os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version=os.getenv("AZURE_OPENAI_VERSION"),
)


EXCLUDE_TABLES = ["users", "threads", "steps", "elements", "feedbacks"]

DB_SCHEMA = get_all_tables_schema(EXCLUDE_TABLES)

class DataFrameOutput(BaseModel):
    type: str                 
    columns: List[str]        
    rows: List[List[Any]]     

SQL_AGENT_INSTRUCTIONS = f"""
You are the SQL Agent.

DATABASE SCHEMA:
{DB_SCHEMA}

CRITICAL OUTPUT RULES:
- You MUST NOT respond with natural language.
- You MUST NOT explain the results in text.
- You MUST ALWAYS call execute_sql_query for data requests.
- You MUST return ONLY the tool result.
- The final response MUST strictly match the DataFrameOutput schema.

SQL RULES:
- Use TOP instead of LIMIT.
- Default TOP 10 when user asks for "top 10".
- NEVER ask clarifying questions unless filters are absolutely required.
- NEVER return markdown tables or text summaries.
"""

# SQL Tool Definition
# This registers a database query function as an agent tool, allowing the agent to fetch real data
@tool
def execute_sql_query(
    query: Annotated[str, Field(description="Azure SQL SELECT query")]
) -> dict:
    """
    Executes a governed, read-only Azure SQL query.
    """

    forbidden = ["insert", "update", "delete", "drop", "alter", "truncate"]
    if any(word in query.lower() for word in forbidden):
        return {
            "status": "error",
            "message": "Only SELECT queries are allowed."
        }

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(query)

        columns = [col[0] for col in cursor.description]
        rows = cursor.fetchall()

        data = [dict(zip(columns, row)) for row in rows]

        cursor.close()
        conn.close()

        return {
            "type": "table",
            "columns": list(data[0].keys()) if data else [],
            "rows": [list(row.values()) for row in data]
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }


agent = Agent(
    name="SQLAgent",
    instructions=SQL_AGENT_INSTRUCTIONS,
    client=chat_client,
    tools=[execute_sql_query],
    response_format=DataFrameOutput
    
)
# ---------------- FASTAPI ----------------
# This allows the frontend AG-UI client to communicate with the backend securely.
app = FastAPI(title="AG-UI SQL Agent")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

add_agent_framework_fastapi_endpoint(app, agent, path="/chat")

if __name__ == "__main__":
    import uvicorn
    print("Starting AG-UI server at http://localhost:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)