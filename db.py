import os
import pyodbc

def get_db_connection():
    conn = pyodbc.connect(
        f"DRIVER={os.getenv('AZURE_SQL_DRIVER')};"
        f"SERVER={os.getenv('AZURE_SQL_SERVER')};"
        f"DATABASE={os.getenv('AZURE_SQL_DATABASE')};"
        f"UID={os.getenv('AZURE_SQL_USERNAME')};"
        f"PWD={os.getenv('AZURE_SQL_PASSWORD')};"
        "Encrypt=yes;"
        "TrustServerCertificate=no;"
        "Connection Timeout=30;"
    )
    return conn


def get_all_tables_schema(exclude_tables=None):
    """
    Returns schema info similar to SK injection style
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT TABLE_SCHEMA, TABLE_NAME, COLUMN_NAME, DATA_TYPE
        FROM INFORMATION_SCHEMA.COLUMNS
        ORDER BY TABLE_SCHEMA, TABLE_NAME
    """)

    tables = {}
    for schema, table, column, dtype in cursor.fetchall():
        if exclude_tables and table in exclude_tables:
            continue

        key = f"{schema}.{table}"
        tables.setdefault(key, []).append(f"{column} ({dtype})")

    cursor.close()
    conn.close()

    schema_text = ""
    for table, cols in tables.items():
        schema_text += f"\nTable: {table}\n"
        for col in cols:
            schema_text += f"  - {col}\n"

    return schema_text