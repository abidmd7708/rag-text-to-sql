from .bm25_retriever import search_bm25


if __name__ == "__main__":

    query = "Which customers spent the most money?"

    print("Query:")
    print(query)

    print("\nBM25 results:")
    print("=" * 70)

    results = search_bm25(
        query,
        top_k=5
    )

    for i, result in enumerate(results, start=1):

        print(f"\nRank: {i}")
        print(f"ID: {result['id']}")
        print(f"Type: {result['type']}")
        print(f"Score: {result['score']}")
        print("Document:")
        print(result["text"])