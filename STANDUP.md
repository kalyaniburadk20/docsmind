# Daily Standups

  ## 2026-06-11 (Day 4)
  Yesterday: Ollama smoke tests + embedding model debugging (PR #9, #10)
  Today:     PDF loading + chunking pipeline (PR #?)
  Blockers:  none
  Notes:
    - PyPDFLoader produces one Document per page; splitter then merges
      across pages with overlap.
    - Chose chunk_size=500, overlap=80 as starting defaults; tested
      200/30 and 1500/200 to feel the trade-off.
      
  ## 2026-06-09 (Day 3)
  Yesterday: backend skeleton + /health route (PR #N)
  Today:     ChatOllama + OllamaEmbeddings smoke tests; cosine sim experiment
  Blockers:  none
  Note:      embedding similarity experiment made retrieval click — sim(rag, rag)=0.75 vs sim(rag, pasta)=0.35
  
  ## 2026-06-03 (Day 2)
  Yesterday: Ollama install + repo scaffolding (tickets #1, #2)
  Today:     Python skeleton + FastAPI /health (tickets #3, #4)
  Blockers:  none
  
  ## 2026-06-01 (Day 1)
- Repo created
- Milestones created
- Sprint 1 tickets created
- Install Ollama

Blockers:
- None

- Tomorrow: ticket #2 — close out repo setup, start ticket #3 (Python skeleton
