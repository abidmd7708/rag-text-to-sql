from .documents import load_all_documents


if __name__ == "__main__":

    documents = load_all_documents()

    print(f"Total documents: {len(documents)}")

    for document in documents:

        print("\n" + "=" * 60)

        print("ID:", document["id"])
        print("TYPE:", document["type"])

        print(document["text"])