from .vector_store import search_similar_documents


if __name__ == "__main__":

    query = "Which customers spent the most money?"

    for document_type in [
        "schema",
        "example",
        "business_rule"
    ]:

        print("\n")
        print("=" * 70)
        print(f"TYPE: {document_type}")
        print("=" * 70)

        results = search_similar_documents(
            query,
            top_k=3,
            document_type=document_type
        )

        for i in range(len(results["ids"][0])):

            print(f"\nRank: {i + 1}")
            print(f"ID: {results['ids'][0][i]}")
            print(f"Distance: {results['distances'][0][i]}")
            print(results["documents"][0][i])