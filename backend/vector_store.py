import chromadb

from .documents import load_all_documents
from .embeddings import create_embedding


CHROMA_PATH = "data/chroma"

client = chromadb.PersistentClient(
    path=CHROMA_PATH
)

collection = client.get_or_create_collection(
    name="text2sql_knowledge"
)


def build_vector_store():

    documents = load_all_documents()

    ids = []
    texts = []
    metadatas = []
    embeddings = []

    for document in documents:

        print(f"Embedding: {document['id']}")

        ids.append(document["id"])
        texts.append(document["text"])

        metadatas.append({
            "type": document["type"],
            **document["metadata"]
        })

        embeddings.append(
            create_embedding(document["text"])
        )

    collection.upsert(
        ids=ids,
        documents=texts,
        metadatas=metadatas,
        embeddings=embeddings
    )

    print()
    print("Vector store built successfully.")
    print("Documents stored:", collection.count())


def search_similar_documents(
    query,
    top_k=5,
    document_type=None
):

    query_embedding = create_embedding(query)

    query_kwargs = {
        "query_embeddings": [query_embedding],
        "n_results": top_k
    }

    if document_type:
        query_kwargs["where"] = {
            "type": document_type
        }

    results = collection.query(
        **query_kwargs
    )

    return results