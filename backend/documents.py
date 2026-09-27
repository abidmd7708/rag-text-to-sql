import json
from pathlib import Path

from .schema import get_database_schema


def load_schema_documents():
    schema = get_database_schema()

    documents = []

    for table_name, columns in schema.items():

        column_text = "\n".join(
            f"- {column['column']} ({column['type']})"
            for column in columns
        )

        text = f"""
Table: {table_name}

Columns:
{column_text}
""".strip()

        documents.append({
            "id": f"schema_{table_name}",
            "type": "schema",
            "text": text,
            "metadata": {
                "table": table_name
            }
        })

    return documents


def load_example_documents():

    path = Path("data/examples/examples.json")

    with open(path, "r", encoding="utf-8") as file:
        examples = json.load(file)

    documents = []

    for example in examples:

        text = f"""
Question:
{example['question']}

SQL:
{example['sql']}
""".strip()

        documents.append({
            "id": example["id"],
            "type": "example",
            "text": text,
            "metadata": {
                "question": example["question"]
            }
        })

    return documents


def load_business_rule_documents():

    path = Path("data/business_rules/rules.json")

    with open(path, "r", encoding="utf-8") as file:
        rules = json.load(file)

    documents = []

    for rule in rules:

        documents.append({
            "id": rule["id"],
            "type": "business_rule",
            "text": rule["rule"],
            "metadata": {}
        })

    return documents


def load_all_documents():

    return (
        load_schema_documents()
        + load_example_documents()
        + load_business_rule_documents()
    )