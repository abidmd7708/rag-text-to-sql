import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification


MODEL_NAME = "BAAI/bge-reranker-v2-m3"

device = "cuda" if torch.cuda.is_available() else "cpu"

print(f"Loading reranker on: {device}")

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

model = AutoModelForSequenceClassification.from_pretrained(
    MODEL_NAME
)

model.to(device)
model.eval()


def rerank(query, documents, top_k=5):
    pairs = []

    for document in documents:
        pairs.append([
            query,
            document["text"]
        ])

    inputs = tokenizer(
        pairs,
        padding=True,
        truncation=True,
        return_tensors="pt"
    )

    inputs = {
        key: value.to(device)
        for key, value in inputs.items()
    }

    with torch.no_grad():
        outputs = model(**inputs)

    scores = outputs.logits.view(-1).float()

    ranked_documents = []

    for document, score in zip(documents, scores):
        result = document.copy()
        result["reranker_score"] = float(score)
        ranked_documents.append(result)

    ranked_documents.sort(
        key=lambda x: x["reranker_score"],
        reverse=True
    )

    return ranked_documents[:top_k]