from db import get_all_tables_schema

def build_schema_text():
    schema = get_all_tables_schema(exclude_tables=[
        "users", "threads", "steps", "elements", "feedbacks"
    ])

    text_blocks = []
    for table, cols in schema.items():
        cols_text = ", ".join(cols)
        text_blocks.append(
            f"Table {table} contains columns: {cols_text}"
        )

    return "\n".join(text_blocks)