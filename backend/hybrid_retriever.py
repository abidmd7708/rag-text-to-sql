from .vector_store import search_similar_documents
from .bm25_retriever import search_bm25


def reciprocal_rank_fusion(
    dense_results,
    bm25_results,
    k=60
):

    scores = {}
    documents = {}

    # Dense results
    for rank, result_id in enumerate(
        dense_results["ids"][0],
        start=1
    ):

        score = 1 / (k + rank)

        scores[result_id] = (
            scores.get(result_id, 0) + score
        )

        documents[result_id] = {
            "id": result_id,
            "type": dense_results["metadatas"][0][rank - 1]["type"],
            "text": dense_results["documents"][0][rank - 1]
        }

    # BM25 results
    for rank, result in enumerate(
        bm25_results,
        start=1
    ):

        result_id = result["id"]

        score = 1 / (k + rank)

        scores[result_id] = (
            scores.get(result_id, 0) + score
        )

        if result_id not in documents:

            documents[result_id] = {
                "id": result_id,
                "type": result["type"],
                "text": result["text"]
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


def hybrid_search_all_types(
    query,
    top_k_per_type=5
):

    results = {}

    for document_type in [
        "schema",
        "example",
        "business_rule"
    ]:

        results[document_type] = hybrid_search_by_type(
            query,
            document_type,
            top_k=top_k_per_type
        )

    return results