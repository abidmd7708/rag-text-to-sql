from .vector_store import search_similar_documents


if __name__ == "__main__":

    query = "Which customers spent the most money?"

    print("Query:")
    print(query)

    print("\nTop retrieved documents:")
    print("=" * 70)

    results = search_similar_documents(
        query,
        top_k=5
    )

    ids = results["ids"][0]
    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    for i in range(len(ids)):

        print(f"\nRank: {i + 1}")
        print(f"ID: {ids[i]}")
        print(f"Type: {metadatas[i]['type']}")
        print(f"Distance: {distances[i]}")
        print("Document:")
        print(documents[i])