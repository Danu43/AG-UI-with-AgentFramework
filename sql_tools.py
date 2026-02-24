from typing import Annotated
from pydantic import Field
from agent_framework import tool
from db import get_db_connection

@tool
def execute_sql_query(
    query: Annotated[str, Field(description="Azure SQL SELECT query")]
) -> dict:
    """
    Executes a governed, read-only Azure SQL query.
    """

    print("\n================ SQL TOOL CALLED ================")
    print("QUERY:")
    print(query)
    print("================================================\n")

    forbidden = ["insert", "update", "delete", "drop", "alter", "truncate"]
    if any(word in query.lower() for word in forbidden):
        print("❌ BLOCKED NON-SELECT QUERY")
        return {
            "type": "error",
            "message": "Only SELECT queries are allowed."
        }

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(query)

        columns = [col[0] for col in cursor.description]
        rows = cursor.fetchall()

        # ---- PRINT TABLE IN TERMINAL ----
        print("✅ QUERY EXECUTED SUCCESSFULLY")
        print("COLUMNS:")
        print(columns)
        print("\nROWS (first 10):")
        for r in rows[:10]:
            print(list(r))

        print(f"\nTOTAL ROWS: {len(rows)}")
        print("===============================================\n")

        cursor.close()
        conn.close()

        return {
            "type": "table",
            "columns": columns,
            "rows" : rows
        }

    except Exception as e:
        print("❌ SQL EXECUTION ERROR:", str(e))
        return {
            "type": "error",
            "message": str(e)
        }