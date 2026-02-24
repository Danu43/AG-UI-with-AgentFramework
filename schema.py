# # db/schema.py
# import pyodbc
# import os

# AZURE_SQL_SERVER = os.getenv("AZURE_SQL_SERVER")
# AZURE_SQL_DATABASE = os.getenv("AZURE_SQL_DATABASE")
# AZURE_SQL_USERNAME = os.getenv("AZURE_SQL_USERNAME")
# AZURE_SQL_PASSWORD = os.getenv("AZURE_SQL_PASSWORD")

# # def get_db_connection():
# #     return pyodbc.connect(
# #         f"DRIVER={{ODBC Driver 17 for SQL Server}};"
# #         f"SERVER={AZURE_SQL_SERVER};"
# #         f"DATABASE={AZURE_SQL_DATABASE};"
# #         f"UID={AZURE_SQL_USERNAME};"
# #         f"PWD={AZURE_SQL_PASSWORD};"
# #         f"Encrypt=yes;"
# #         f"TrustServerCertificate=no;"
# #     )

# def get_all_tables_schema(exclude_tables=None):
#     exclude_tables = exclude_tables or []
#     conn = get_db_connection()
#     cursor = conn.cursor()

#     cursor.execute("""
#         SELECT TABLE_SCHEMA, TABLE_NAME
#         FROM INFORMATION_SCHEMA.TABLES
#         WHERE TABLE_TYPE = 'BASE TABLE'
#     """)
#     tables = cursor.fetchall()

#     schema_info = []

#     for schema, table in tables:
#         if table in exclude_tables:
#             continue

#         cursor.execute("""
#             SELECT COLUMN_NAME, DATA_TYPE
#             FROM INFORMATION_SCHEMA.COLUMNS
#             WHERE TABLE_SCHEMA = ? AND TABLE_NAME = ?
#         """, (schema, table))

#         columns = cursor.fetchall()
#         schema_info.append({
#             "schema": schema,
#             "table": table,
#             "columns": {c[0]: c[1] for c in columns}
#         })

#     conn.close()
#     return schema_info