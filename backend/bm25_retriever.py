import re

from rank_bm25 import BM25Okapi

from .documents import load_all_documents


documents = load_all_documents()


def tokenize(text):
    return re.findall(
        r"\b\w+\b",
        text.lower()
    )


def create_bm25_index(document_list):
    corpus = [
        tokenize(document["text"])
        for document in document_list
    ]

    return BM25Okapi(corpus)


def search_bm25(query, top_k=5, document_type=None):

    if document_type:
        filtered_documents = [
            document
            for document in documents
            if document["type"] == document_type
        ]
    else:
        filtered_documents = documents

    if not filtered_documents:
        return []

    bm25 = create_bm25_index(filtered_documents)

    query_tokens = tokenize(query)

    scores = bm25.get_scores(query_tokens)

    ranked_indices = sorted(
        range(len(scores)),
        key=lambda i: scores[i],
        reverse=True
    )[:top_k]

    results = []

    for index in ranked_indices:

        document = filtered_documents[index]

        results.append({
            "id": document["id"],
            "type": document["type"],
            "text": document["text"],
            "score": float(scores[index])
        })

    return results