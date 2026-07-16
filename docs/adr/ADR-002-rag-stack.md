# ADR-002: Knowledge Representation

**Status:** Accepted  
**Date:** 2026-07-16

## Context

During dataset exploration, we analyzed both `products.csv` and `reviews.csv` to determine the most suitable knowledge representation for the RAG pipeline.

### Key Findings

- **728** products
- **6,327** customer reviews
- **700** products have reviews (**96.15% coverage**)
- **28** products have no reviews
- **0** orphan reviews (referential integrity maintained)
- Relationship between datasets is **One Product → Many Reviews (1:N)**
- Average reviews per product: **9.04**
- Maximum reviews per product: **19**

---

## Decision

The knowledge base will use:

> **One Product = One  Document +  Metadata**

The separation between document content and metadata is an intentional architectural decision made to improve scalability, retrieval efficiency, and maintainability, even though the current dataset size would allow a simpler design.

Each document will consolidate:

- Product information
- Product description
- Product attributes
- Customer review summary (subject to preprocessing)
- All associated customer reviews

Each Metadata will contain:
- ASIN
- Brand
- Price 
- Category
- Rating


---

## Scalability Considerations

Although the current dataset contains only **728 products**, the project adopts a ** Document +  Metadata** architecture to align with production-scale Retrieval-Augmented Generation (RAG) systems.

For a small corpus, storing all information inside the document would still produce acceptable results. However, separating semantic content from structured metadata provides a more scalable and maintainable design.

This approach enables:

- Efficient metadata filtering (e.g., brand, category, price range, rating)
- Faster retrieval by reducing the search space before semantic search
- Better compatibility with vector databases that support metadata-based filtering
- Clear separation between semantic information and structured attributes
- Easier extension to larger datasets without redesigning the retrieval pipeline

The architecture is therefore designed not only to satisfy the current project requirements but also to demonstrate production-oriented engineering practices.

## Consequences

### Advantages

- Simpler retrieval pipeline
- Self-contained knowledge units
- Easier prompt construction
- Reduced retrieval orchestration
- Better user-centric document representation

### Trade-offs

- Some products generate large documents.
- Chunking is required before embedding.

---