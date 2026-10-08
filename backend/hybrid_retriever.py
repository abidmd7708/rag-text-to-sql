from .vector_store import search_similar_documents,collection
from .bm25_retriever import search_bm25
from .graph_retriever import expand_tables


def reciprocal_rank_fusion(dense_results, bm25_results, k=60):
    scores = {}
    documents = {}

    for rank, result_id in enumerate(
        dense_results["ids"][0],
        start=1
    ):
        score = 1 / (k + rank)

        scores[result_id] = scores.get(result_id, 0) + score

        documents[result_id] = {
            "id": result_id,
            "type": dense_results["metadatas"][0][rank - 1]["type"],
            "text": dense_results["documents"][0][rank - 1],
        }

    for rank, result in enumerate(
        bm25_results,
        start=1
    ):
        result_id = result["id"]

        score = 1 / (k + rank)

        scores[result_id] = scores.get(result_id, 0) + score

        if result_id not in documents:
            documents[result_id] = {
                "id": result_id,
                "type": result["type"],
                "text": result["text"],
            }

    ranked_ids = sorted(
        scores,
        key=scores.get,
        reverse=True
    )

    results = []

    for result_id in ranked_ids:

        result = documents[result_id].copy()

        result["rrf_score"] = scores[result_id]

        results.append(result)

    return results


def hybrid_search_by_type(
    query,
    document_type,
    top_k=5
):
    dense_results = search_similar_documents(
        query,
        top_k=top_k,
        document_type=document_type
    )

    bm25_results = search_bm25(
        query,
        top_k=top_k,
        document_type=document_type
    )

    return reciprocal_rank_fusion(
        dense_results,
        bm25_results
    )[:top_k]


def extract_table_name(document):
    """
    Extract table name from a schema document.

    Example:

        Table: customers

    returns:

        customers
    """

    import re

    match = re.search(
        r"Table:\s*(\w+)",
        document["text"],
        flags=re.IGNORECASE
    )

    if match:
        return match.group(1)

    return None


def graph_expand_schema_results(schema_results, max_hops=2):
    initial_tables = []

    for document in schema_results:
        table_name = extract_table_name(document)
        if table_name:
            initial_tables.append(table_name)

    if not initial_tables:
        return schema_results

    expanded_tables = expand_tables(
        initial_tables,
        max_hops=max_hops
    )

    existing_tables = set(initial_tables)
    expanded_documents = list(schema_results)

    for table_name in expanded_tables:

        if table_name in existing_tables:
            continue

        schema_id = f"schema_{table_name}"

        result = collection.get(
            ids=[schema_id],
            include=["documents", "metadatas"]
        )

        if not result["ids"]:
            continue

        expanded_documents.append({
            "id": result["ids"][0],
            "type": "schema",
            "text": result["documents"][0],
            "metadata": result["metadatas"][0],
            "rrf_score": 0.0,
            "graph_expanded": True,
        })

    return expanded_documents

def hybrid_search_all_types(
    query,
    top_k_per_type=5
):
    results = {}

    # Stage 1 + Stage 2:
    # Dense + BM25 -> RRF

    schema_results = hybrid_search_by_type(
        query,
        "schema",
        top_k=top_k_per_type
    )

    example_results = hybrid_search_by_type(
        query,
        "example",
        top_k=top_k_per_type
    )

    rule_results = hybrid_search_by_type(
        query,
        "business_rule",
        top_k=top_k_per_type
    )

    # Stage 3:
    # Graph expansion applies only to schema.

    schema_results = graph_expand_schema_results(
        schema_results,
        max_hops=2
    )

    results["schema"] = schema_results
    results["example"] = example_results
    results["business_rule"] = rule_results

    return results