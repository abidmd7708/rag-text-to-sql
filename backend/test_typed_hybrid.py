from .hybrid_retriever import hybrid_search_all_types


if __name__ == "__main__":

    query = "Which customers spent the most money?"

    results = hybrid_search_all_types(
        query,
        top_k_per_type=3
    )

    for document_type, documents in results.items():

        print("\n")
        print("=" * 70)
        print(f"TYPE: {document_type}")
        print("=" * 70)

        for rank, document in enumerate(
            documents,
            start=1
        ):

            print(f"\nRank: {rank}")
            print(f"ID: {document['id']}")
            print(f"RRF Score: {document['rrf_score']}")
            print("Document:")
            print(document["text"])