"""Smoke test: call the local Llama 3.2 model via Ollama and print one response.

Run from the backend/ folder with the venv active:
    python scripts/test_chat.py
"""
from langchain_ollama import ChatOllama


def main() -> None:
    # temperature=0 makes the output deterministic — good for testing.
    llm = ChatOllama(model="llama3.2:3b", temperature=0)

    prompt = "Explain what RAG (Retrieval-Augmented Generation) is, in two sentences."
    print(f"Prompt:\n  {prompt}\n")

    response = llm.invoke(prompt)
    print(f"Response:\n  {response.content}\n")


if __name__ == "__main__":
    main()