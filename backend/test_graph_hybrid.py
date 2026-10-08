from .hybrid_retriever import hybrid_search_all_types


if __name__ == "__main__":

    question = "Which customers spent the most money?"

    results = hybrid_search_all_types(
        question,
        top_k_per_type=3
    )

    print("\n" + "=" * 70)
    print("HYBRID + GRAPH RETRIEVAL")
    print("=" * 70)

    for document_type, documents in results.items():

        print(f"\n\n{document_type.upper()}")
        print("-" * 70)

        for rank, document in enumerate(
            documents,
            start=1
        ):

            print(
                f"{rank}. "
                f"{document['id']}"
            )

            if "rrf_score" in document:
                print(
                    f"   RRF: "
                    f"{document['rrf_score']:.5f}"
                )

            if document.get(
                "graph_expanded",
                False
            ):
                print(
                    "   SOURCE: GRAPH EXPANSION"
                )

            print(
                f"   {document['text'][:150]}"
            )