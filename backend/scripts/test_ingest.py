"""Smoke test: load a PDF and split it into chunks.

Run from the backend/ folder with the venv active:
    python scripts/test_ingest.py
"""
from pathlib import Path
import re

def normalize_text(text: str) -> str:
    """Clean up PDF extraction artifacts.

    Common issues from Google Docs / various PDF producers:
    - words on separate lines: "submit\n \nresponses"  -> "submit responses"
    - double/multiple spaces:  "desktop  computers"    -> "desktop computers"
    - excessive blank lines:   "para1\n\n\n\npara2"    -> "para1\n\npara2"
    """
    # Collapse "\n \n" (line, space, line) into a single space.
    text = re.sub(r"\n\s*\n", "\n\n", text)             # normalize paragraph breaks
    text = re.sub(r"(?<!\n)\n(?!\n)", " ", text)        # single newlines → spaces
    text = re.sub(r"[ \t]+", " ", text)                 # multiple spaces → one space
    return text.strip()

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


PDF_PATH = Path("sample_data/sample.pdf")
CHUNK_SIZE = 500          # characters per chunk (roughly ~100-150 tokens)
CHUNK_OVERLAP = 80        # characters of overlap between adjacent chunks


def main() -> None:
    if not PDF_PATH.exists():
        raise FileNotFoundError(
            f"Place a test PDF at {PDF_PATH}. See Day 4 instructions."
        )

    # 1. Load: produces one Document per PAGE.
    loader = PyPDFLoader(str(PDF_PATH))
    pages = loader.load()
    print(f"Loaded {len(pages)} pages from {PDF_PATH.name}")

    pages = loader.load()
for page in pages:
    page.page_content = normalize_text(page.page_content)
print(f"Loaded {len(pages)} pages from {PDF_PATH.name}")

    # 2. Split: produces overlapping chunks across all pages.
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        # RecursiveCharacterTextSplitter tries these separators in order,
        # so it prefers to break at paragraph > line > sentence > word > char.
        separators=["\n\n", "\n", ". ", " ", ""],
    )
    chunks = splitter.split_documents(pages)
    print(f"Produced {len(chunks)} chunks "
          f"(chunk_size={CHUNK_SIZE}, overlap={CHUNK_OVERLAP})")

    # 3. Inspect: stats and the first few chunks.
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