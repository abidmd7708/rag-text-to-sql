from .hybrid_retriever import hybrid_search_all_types
from .reranker import rerank


if __name__ == "__main__":

    query = "Which customers spent the most money?"

    retrieved = hybrid_search_all_types(
        query,
        top_k_per_type=3
    )

    candidates = []

    for document_type, documents in retrieved.items():
        candidates.extend(documents)

    print("\nTotal candidates:", len(candidates))

    print("\n" + "=" * 70)
    print("RERANKED RESULTS")
    print("=" * 70)

    results = rerank(
        query,
        candidates,
        top_k=5
    )

    for rank, document in enumerate(results, start=1):

        print(f"\nRank: {rank}")
        print(f"ID: {document['id']}")
        print(f"Type: {document['type']}")
        print(f"RRF Score: {document['rrf_score']}")
        print(f"Reranker Score: {document['reranker_score']}")
        print("\nDocument:")
        print(document["text"])