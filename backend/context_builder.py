import re

from .hybrid_retriever import hybrid_search_all_types
from .reranker import rerank
from .vector_store import search_similar_documents


def extract_tables_from_sql(sql):
    """
    Extract table names appearing after FROM and JOIN.
    """

    pattern = r"\b(?:FROM|JOIN)\s+([a-zA-Z_][a-zA-Z0-9_]*)"

    tables = re.findall(
        pattern,
        sql,
        flags=re.IGNORECASE
    )

    return list(dict.fromkeys(tables))


def get_schema_for_tables(table_names):
    """
    Retrieve schema documents for the required tables.
    """

    schema_documents = []

    for table_name in table_names:

        results = search_similar_documents(
            f"Table {table_name}",
            top_k=1,
            document_type="schema"
        )

        if results["ids"][0]:

            document = {
                "id": results["ids"][0][0],
                "type": "schema",
                "text": results["documents"][0][0],
            }

            schema_documents.append(document)

    return schema_documents


def retrieve_context(query, top_k_per_type=3):
    """
    Dense + BM25 → RRF → Reranker → Schema Expansion
    """

    # --------------------------------------------------
    # 1. Hybrid retrieval
    # --------------------------------------------------

    retrieved = hybrid_search_all_types(
        query,
        top_k_per_type=top_k_per_type
    )

    # --------------------------------------------------
    # 2. Combine candidates
    # --------------------------------------------------

    candidates = []

    for document_type, documents in retrieved.items():
        candidates.extend(documents)

    # --------------------------------------------------
    # 3. Rerank
    # --------------------------------------------------

    reranked = rerank(
        query,
        candidates,
        top_k=len(candidates)
    )

    # --------------------------------------------------
    # 4. Select examples
    # --------------------------------------------------

    selected_examples = []

    for document in reranked:

        if (
            document["type"] == "example"
            and len(selected_examples) < 2
        ):
            selected_examples.append(document)

    # --------------------------------------------------
    # 5. Select business rules
    # --------------------------------------------------

    selected_rules = []

    for document in reranked:

        if (
            document["type"] == "business_rule"
            and len(selected_rules) < 2
        ):
            selected_rules.append(document)

    # --------------------------------------------------
    # 6. Extract tables from retrieved examples
    # --------------------------------------------------

    required_tables = set()

    for example in selected_examples:

        sql = example["text"]

        tables = extract_tables_from_sql(sql)

        required_tables.update(tables)

    # --------------------------------------------------
    # 7. Add directly retrieved schema tables
    # --------------------------------------------------

    for document in reranked:

        if document["type"] == "schema":

            table_match = re.search(
                r"Table:\s*(\w+)",
                document["text"],
                flags=re.IGNORECASE
            )

            if table_match:
                required_tables.add(
                    table_match.group(1)
                )

    # --------------------------------------------------
    # 8. Retrieve schema for all required tables
    # --------------------------------------------------

    schema_documents = get_schema_for_tables(
        required_tables
    )

    return {
        "schema": schema_documents,
        "example": selected_examples,
        "business_rule": selected_rules
    }


def build_context_prompt(query):

    context = retrieve_context(query)

    prompt_parts = []

    # --------------------------------------------------
    # DATABASE SCHEMA
    # --------------------------------------------------

    prompt_parts.append("DATABASE SCHEMA")
    prompt_parts.append("=" * 50)

    for document in context["schema"]:
        prompt_parts.append(
            document["text"]
        )

    # --------------------------------------------------
    # EXAMPLES
    # --------------------------------------------------

    prompt_parts.append(
        "\nRELEVANT EXAMPLES"
    )

    prompt_parts.append(
        "=" * 50
    )

    for document in context["example"]:
        prompt_parts.append(
            document["text"]
        )

    # --------------------------------------------------
    # BUSINESS RULES
    # --------------------------------------------------

    prompt_parts.append(
        "\nBUSINESS RULES"
    )

    prompt_parts.append(
        "=" * 50
    )

    for document in context["business_rule"]:
        prompt_parts.append(
            f"- {document['text']}"
        )

    # --------------------------------------------------
    # USER QUESTION
    # --------------------------------------------------

    prompt_parts.append(
        "\nUSER QUESTION"
    )

    prompt_parts.append(
        "=" * 50
    )

    prompt_parts.append(query)

    return "\n\n".join(prompt_parts)