from .embeddings import create_embedding


if __name__ == "__main__":

    text = "customers who spent the most money"

    print("Generating embedding...")

    embedding = create_embedding(text)

    print("Embedding generated successfully.")
    print("Vector dimensions:", len(embedding))

    print("\nFirst 10 values:")
    print(embedding[:10])