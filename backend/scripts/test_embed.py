"""Smoke test: embed one sentence with nomic-embed-text and inspect the vector.

Run from the backend/ folder with the venv active:
    python scripts/test_embed.py
"""
from langchain_ollama import OllamaEmbeddings


def main() -> None:
    embeddings = OllamaEmbeddings(model="nomic-embed-text")

    sentence = "DocsMind is a local-first RAG agent."
    vector = embeddings.embed_query(sentence)

    print(f"Sentence: {sentence}")
    print(f"Vector length: {len(vector)}")
    print(f"First 5 values: {vector[:5]}")
    print(f"Last 5 values:  {vector[-5:]}")


if __name__ == "__main__":
    main()