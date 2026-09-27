import os
import requests
from dotenv import load_dotenv

from .context_builder import build_context_prompt

load_dotenv()

OLLAMA_URL = os.getenv(
    "OLLAMA_URL",
    "http://localhost:11434"
)

OLLAMA_MODEL = os.getenv(
    "OLLAMA_MODEL",
    "qwen3:8b"
)


def generate_sql(question):

    rag_context = build_context_prompt(question)

    prompt = f"""
Convert the user's question into ONE PostgreSQL SELECT query.

{rag_context}

RULES:
- Return ONLY the SQL query.
- Do not explain.
- Do not use markdown.
- Use only tables and columns provided in DATABASE SCHEMA.
- Use PostgreSQL syntax.
- Follow the BUSINESS RULES.
- Use RELEVANT EXAMPLES as guidance when applicable.
- Return exactly one SELECT statement.
- Do not invent tables or columns.
- Exclude cancelled orders when calculating spending.
- For revenue or customer spending, use only completed orders.
- Customer spending is calculated as product price multiplied by quantity.
- Return only executable SQL.
- Preserve explicit numbers from the user's question.
- If a relevant example contains a specific LIMIT and the user's question does not specify a different number, follow that example's LIMIT.
- Do not arbitrarily change LIMIT values.

SQL:
"""

    response = requests.post(
        f"{OLLAMA_URL}/api/generate",
        json={
            "model": OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False,
            "think": False,
            "options": {
                "temperature": 0,
                "num_predict": 300
            }
        },
        timeout=300
    )

    response.raise_for_status()

    result = response.json()

    print("\nDEBUG - Ollama response:")
    print(result)

    sql = result.get("response", "").strip()

    if not sql:
        raise RuntimeError(
            "Qwen returned an empty response."
        )

    return sql