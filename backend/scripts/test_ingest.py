"""Smoke test: load a PDF, normalize text, and split it into chunks.

Run from the backend/ folder with the venv active:
    python scripts/test_ingest.py
"""
import re
from pathlib import Path

# PyPDFLoader still lives in langchain-community (see langchain migration docs).
# The deprecation warning is informational, not blocking.
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


PDF_PATH = Path("sample_data/sample.pdf")
CHUNK_SIZE = 500          # characters per chunk (roughly ~100-150 tokens)
CHUNK_OVERLAP = 80        # characters of overlap between adjacent chunks


def normalize_text(text: str) -> str:
    """Clean up PDF extraction artifacts.

    Strategy: do single-newline cleanup BEFORE paragraph-break normalization,
    so we don't accidentally collapse word-per-line text into "paragraphs".
    """
    # Step 1: single newlines that are NOT part of a blank-line paragraph break
    # become spaces. This handles "word\nword" -> "word word".
    text = re.sub(r"(?<!\n)\n(?!\n)", " ", text)

    # Step 2: collapse 3+ newlines down to exactly two (a paragraph break).
    text = re.sub(r"\n{3,}", "\n\n", text)

    # Step 3: collapse multiple spaces/tabs into one.
    text = re.sub(r"[ \t]+", " ", text)

    return text.strip()


def main() -> None:
    if not PDF_PATH.exists():
        raise FileNotFoundError(
            f"Place a test PDF at {PDF_PATH}. See Day 4 instructions."
        )

    # 1. Load: produces one Document per PAGE.
    loader = PyPDFLoader(str(PDF_PATH))
    pages = loader.load()
    print(f"Loaded {len(pages)} pages from {PDF_PATH.name}")

    # 2. Normalize: clean up PDF extraction artifacts on each page.
    for page in pages:
        page.page_content = normalize_text(page.page_content)

    # 3. Split: produces overlapping chunks across all pages.
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        # Prefers paragraph > line > sentence > word > char boundaries.
        separators=["\n\n", "\n", ". ", " ", ""],
    )
    chunks = splitter.split_documents(pages)
    print(f"Produced {len(chunks)} chunks "
          f"(chunk_size={CHUNK_SIZE}, overlap={CHUNK_OVERLAP})")

    # 4. Inspect: stats and the first/middle/last chunks.
    lengths = [len(c.page_content) for c in chunks]
    print(f"\nChunk length stats:")
    print(f"  min={min(lengths)}  max={max(lengths)}  avg={sum(lengths)//len(lengths)}")

    print(f"\n--- First chunk ---")
    print(f"  source: {chunks[0].metadata}")
    print(f"  text:   {chunks[0].page_content!r}")

    print(f"\n--- Middle chunk ---")
    mid = len(chunks) // 2
    print(f"  source: {chunks[mid].metadata}")
    print(f"  text:   {chunks[mid].page_content[:200]!r}...")

    print(f"\n--- Last chunk ---")
    print(f"  source: {chunks[-1].metadata}")
    print(f"  text:   {chunks[-1].page_content!r}")


if __name__ == "__main__":
    main()