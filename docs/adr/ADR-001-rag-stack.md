# ADR-001: RAG Technology Stack

**Status**

Accepted

---

## Context

The project aims to build a production-inspired Retrieval-Augmented Generation (RAG) application while meeting the following constraints:

- Complete the MVP within the project deadline.
- Minimize operational costs.
- Demonstrate good software engineering and Data Engineering practices.
- Keep the architecture modular and reproducible.
- Avoid unnecessary framework dependencies.

The system requires three major components:

- Embedding model
- Vector database
- Large Language Model

The selected technologies should provide a balance between simplicity, performance, maintainability, and ease of development.

---

## Decision

The following technology stack has been selected:

| Component | Technology |
|-----------|------------|
| Embedding Model | BAAI/bge-small-en-v1.5 |
| Vector Database | ChromaDB |
| Large Language Model | Google Gemini |
| UI | Streamlit |
| Data Processing | Pandas |
| Package Manager | uv |

Retrieval and generation are intentionally separated.

Document and query embeddings are generated locally using Sentence Transformers, while answer generation is performed using Google Gemini.

---

## Rationale

### Sentence Transformers (BAAI/bge-small-en-v1.5)

Selected because it:

- Runs locally.
- Produces high-quality semantic embeddings.
- Has no API cost.
- Supports reproducible indexing.
- Performs well on retrieval benchmarks.
- Can easily be replaced by another embedding model.

---

### ChromaDB

Selected because it:

- Is lightweight.
- Is open source.
- Integrates well with Python.
- Supports persistent vector storage.
- Is sufficient for an MVP-scale dataset.

---

### Google Gemini

Selected because it:

- Provides a generous free tier.
- Offers high-quality language generation.
- Has a simple Python SDK.
- Reduces development cost.

---

## Future Considerations

The architecture intentionally allows replacing:

- ChromaDB → Qdrant
- Gemini → OpenAI / Claude
- Sentence Transformers → Gemini Embeddings / OpenAI Embeddings

without significant changes to the remaining application.

---

## Status

**Accepted**

**Date:** July 2026