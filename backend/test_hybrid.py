from .hybrid_retriever import hybrid_search


if __name__ == "__main__":

    query = "Which customers spent the most money?"

    print("Query:")
    print(query)

    print("\nHybrid Retrieval Results:")
    print("=" * 70)

    results = hybrid_search(
        query,
        top_k=5
    )

    for i, result in enumerate(results, start=1):

        print(f"\nRank: {i}")
        print(f"ID: {result['id']}")
        print(f"Type: {result['type']}")
        print(f"RRF Score: {result['rrf_score']}")
        print("Document:")
        print(result["text"])