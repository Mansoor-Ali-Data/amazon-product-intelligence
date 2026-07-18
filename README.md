# Executive Summary

The **Amazon Product Intelligence Assistant** is an end-to-end **Retrieval-Augmented Generation (RAG)** application that enables users to explore Amazon products and customer reviews through natural language conversations.

Modern e-commerce platforms contain a vast amount of information distributed across product specifications, pricing, ratings, feature descriptions, and thousands of customer reviews. While this information is valuable, extracting meaningful insights often requires users to manually browse multiple product pages and read large volumes of reviews.

This project addresses that challenge by transforming raw Amazon product and review datasets into a **retrieval-optimized knowledge base**. Instead of relying solely on a Large Language Model's internal knowledge, the system retrieves the most relevant product information from a vector database and uses that retrieved context to generate accurate, grounded, and evidence-based responses.

The project is being developed as part of **LLM Zoomcamp** and serves as a **flagship AI Engineering portfolio project**, showcasing the complete lifecycle of building a modern RAG system—from data preprocessing and document modeling to embedding generation, semantic retrieval, evaluation, and deployment.

Beyond building a functional application, the project emphasizes **production-inspired software engineering practices**, including modular architecture, separation of concerns, configuration-driven development, reproducible workflows, and evaluation-first development. Each stage of the pipeline is designed as an independent, maintainable component that can be improved, tested, and evaluated without affecting the rest of the system.

The final application will enable users to ask natural language questions such as:

The final application will enable users to ask natural language questions such as:

- *Does this shirt run small, large, or true to size?*
- *What are the most frequently mentioned pros and cons in customer reviews?*
- *Compare these two products based on customer feedback and ratings.*
- *Is this product good value for money?*
- *What sizing, color, or quality issues do customers commonly report?*

By combining structured product information with unstructured customer reviews, the Amazon Product Intelligence Assistant demonstrates how Retrieval-Augmented Generation can transform large-scale e-commerce data into an intelligent, trustworthy, and interactive product intelligence system.


# Problem Statement

Online shopping platforms provide customers with an enormous amount of information, including product descriptions, specifications, pricing, ratings, and thousands of customer reviews. While this information is valuable, extracting meaningful insights often requires users to manually browse multiple product pages and read a large volume of reviews before making a purchasing decision.

Traditional keyword-based search systems are effective at locating products that contain specific terms, but they struggle to understand user intent or synthesize information from both structured product attributes and unstructured customer feedback. As a result, answering questions such as *"Does this shirt run true to size?"* or *"What quality issues do customers frequently mention?"* often requires significant manual effort.

Large Language Models (LLMs) can generate fluent responses, but without access to external product knowledge they may produce inaccurate, outdated, or hallucinated information. For product intelligence applications, responses must be grounded in actual product data and customer experiences.

This project addresses these challenges by building a **Retrieval-Augmented Generation (RAG)** system that transforms Amazon product and review data into a searchable knowledge base. Instead of relying solely on the LLM's internal knowledge, the system retrieves the most relevant product information and customer reviews before generating a response, enabling more accurate, context-aware, and evidence-based answers.

# Project Goals

The primary goal of this project is to design and implement a **production-inspired Retrieval-Augmented Generation (RAG) system** that enables users to interact with Amazon product and customer review data through natural language.

Beyond building a functional application, the project aims to demonstrate the complete AI Engineering lifecycle—from raw data processing to retrieval and response generation—while following modern software engineering best practices.

The key objectives of this project are:

- Build a complete end-to-end Retrieval-Augmented Generation (RAG) pipeline.
- Transform structured product data and unstructured customer reviews into a retrieval-optimized knowledge base.
- Develop a modular and maintainable architecture with clear separation of responsibilities across each pipeline stage.
- Apply production-inspired Data Engineering practices for preprocessing, document construction, indexing, and retrieval.
- Implement semantic search using dense vector embeddings and a vector database.
- Generate grounded, evidence-based responses using a Large Language Model.
- Evaluate retrieval quality and response quality using systematic evaluation techniques rather than intuition.
- Build a clean, reproducible, and well-documented codebase suitable for learning, experimentation, and future extension.
- Create a portfolio-quality AI Engineering project that demonstrates practical experience with modern RAG systems.

# Dataset Overview

The Amazon Product Intelligence Assistant is built on an Amazon **Products & Reviews** dataset that combines **structured product metadata** with **unstructured customer reviews**. Together, these datasets provide both factual product information and real-world customer experiences, making them well suited for building a Retrieval-Augmented Generation (RAG) system.

The project uses two primary datasets that are linked through a common product identifier, allowing product information and customer reviews to be combined during document construction.

---

## Products Dataset

The products dataset contains structured information describing each product and serves as the authoritative source for product metadata.

Key information includes:

- Product title
- Brand and manufacturer
- Product category hierarchy
- Product features and descriptions
- Pricing information
- Customer ratings and rating count
- Best sellers rank
- Seller information
- Product variants (e.g., size and color)

This structured data provides factual information that forms the foundation of the product knowledge base.

---

## Reviews Dataset

The reviews dataset contains customer-generated feedback that captures real-world experiences with each product.

Key information includes:

- Review title
- Review text
- Customer rating
- Verified purchase status
- Helpful vote count
- Product variant (size and color)
- Sentiment score

Unlike the products dataset, review data is unstructured and provides valuable insights into product quality, sizing, comfort, durability, value for money, and common customer concerns.

---

## Relationship Between the Datasets

Each product can have multiple customer reviews, forming a **one-to-many relationship** between the products and reviews datasets.

```text
Product
   │
   ├── Review 1
   ├── Review 2
   ├── Review 3
   ├── ...
   └── Review N
```

This relationship enables the system to combine structured product metadata with customer experiences when constructing retrieval documents.

---

## Why This Dataset is Suitable for RAG

The dataset combines two complementary sources of information:

- **Structured product metadata** provides factual information such as specifications, pricing, brand, and ratings.
- **Unstructured customer reviews** capture subjective experiences, opinions, and real-world usage that cannot be represented through structured attributes alone.

By integrating these two sources into a unified knowledge base, the system can answer questions that require both factual product information and insights derived from customer feedback.

For example, the system can answer questions such as:

- *Does this shirt run true to size?*
- *What quality issues do customers frequently mention?*
- *Do customers think this product is worth the price?*
- *What features receive the most positive feedback?*

These types of questions cannot be answered reliably using structured product attributes alone, making the dataset an excellent fit for Retrieval-Augmented Generation.

# System Architecture

The Amazon Product Intelligence Assistant follows a **modular, production-inspired architecture** that separates data preparation, knowledge base construction, retrieval, and response generation into independent components.

This separation of concerns makes the system easier to maintain, evaluate, and extend while allowing each stage of the pipeline to evolve independently.

At a high level, the system consists of four logical layers:

1. **Data Processing Pipeline**
2. **Knowledge Base Construction Pipeline**
3. **Online RAG Pipeline**
4. **Evaluation & Observability**

---

## High-Level Architecture

```text
                         Amazon Products & Reviews Dataset
                                      │
                                      ▼
                          ┌────────────────────────┐
                          │   Data Preprocessing   │
                          └────────────────────────┘
                                      │
                                      ▼
                          ┌────────────────────────┐
                          │   Document Modeling    │
                          └────────────────────────┘
                                      │
                                      ▼
                          ┌────────────────────────┐
                          │   Document Builder     │
                          └────────────────────────┘
                                      │
                                      ▼
                          ┌────────────────────────┐
                          │      Chunking          │
                          └────────────────────────┘
                                      │
                                      ▼
                          ┌────────────────────────┐
                          │ Embedding Generation   │
                          └────────────────────────┘
                                      │
                                      ▼
                          ┌────────────────────────┐
                          │     ChromaDB Index     │
                          └────────────────────────┘
                                      ▲
                                      │
                         ─────────────┼─────────────
                                      │
                                      ▼
                                User Question
                                      │
                                      ▼
                          ┌────────────────────────┐
                          │   Query Embedding      │
                          └────────────────────────┘
                                      │
                                      ▼
                          ┌────────────────────────┐
                          │ Semantic Retrieval     │
                          └────────────────────────┘
                                      │
                                      ▼
                          ┌────────────────────────┐
                          │   Prompt Builder       │
                          └────────────────────────┘
                                      │
                                      ▼
                          ┌────────────────────────┐
                          │    Google Gemini       │
                          └────────────────────────┘
                                      │
                                      ▼
                               Grounded Response
```

---

## 1. Data Processing Pipeline

The data processing pipeline transforms the raw Amazon datasets into clean, structured datasets suitable for downstream document construction.

Responsibilities include:

- Removing irrelevant metadata
- Normalizing textual fields
- Repairing malformed records
- Parsing product variants
- Converting true numeric fields
- Preserving business semantics

The output of this stage is a consistent, high-quality dataset that serves as the foundation for the remainder of the pipeline.

---

## 2. Knowledge Base Construction Pipeline

The knowledge base construction pipeline converts processed tabular data into retrieval-optimized documents.

This stage includes:

- Document modeling
- Document generation
- Chunking
- Metadata attachment
- Embedding generation
- Vector indexing

Rather than embedding raw CSV rows, the system constructs semantically meaningful documents that combine structured product metadata with relevant customer review information. These documents are then divided into chunks, converted into dense vector embeddings, and stored in ChromaDB for efficient semantic retrieval.

---

## 3. Online RAG Pipeline

When a user submits a question, the system follows a Retrieval-Augmented Generation workflow.

The process consists of:

1. Converting the user query into a vector embedding.
2. Performing semantic similarity search against ChromaDB.
3. Retrieving the most relevant document chunks.
4. Constructing a grounded prompt using the retrieved context.
5. Generating a final response using Google Gemini.

Because the language model receives retrieved evidence alongside the user's question, responses remain grounded in the product dataset rather than relying solely on the model's internal knowledge.

---

## 4. Evaluation & Observability

Evaluation is treated as a first-class component of the system rather than an afterthought.

The project will evaluate both retrieval quality and response quality throughout development.

Planned evaluation includes:

- Retrieval relevance
- Chunking strategy comparison
- Embedding model comparison
- Prompt evaluation
- Answer quality assessment
- End-to-end RAG evaluation

The project also incorporates structured logging and monitoring to support debugging, reproducibility, and future system improvements.

---

## Architectural Principles

The system is designed around several core engineering principles:

- **Separation of Concerns** – Each pipeline stage has a single, well-defined responsibility.
- **Modularity** – Components can be developed, tested, and replaced independently.
- **Reproducibility** – The entire pipeline can be rebuilt from raw data using configuration-driven workflows.
- **Evaluation-Driven Development** – Design decisions are validated through measurable evaluation rather than intuition.
- **Production-Inspired Design** – The architecture mirrors the structure of real-world AI applications while remaining approachable for learning and experimentation.

# Repository Structure

The project follows a modular, production-inspired repository structure that separates data, configuration, application logic, and supporting resources. This organization improves maintainability, scalability, and reproducibility while keeping individual components focused on a single responsibility.

```text
amazon-product-intelligence/
│
├── app/                        # Streamlit user interface
│
├── config/                     # Project configuration
│   ├── logging.py
│   └── preprocessing_config.yml
│
├── data/
│   ├── raw/                    # Original Amazon datasets
│   ├── processed/              # Cleaned datasets after preprocessing
│   ├── documents/              # Generated product documents
│   ├── chunks/                 # Chunked documents for embeddings
│   ├── embeddings/             # Generated vector embeddings
│   └── evaluation/             # Evaluation datasets and results
│
├── docs/                       # Project documentation & architecture diagrams
│
├── logs/                       # Application logs
│
├── notebooks/                  # Exploratory analysis and experiments
│
├── scripts/                    # Executable pipeline entry points
│   ├── preprocess_data.py
│   ├── build_documents.py
│   ├── build_embeddings.py
│   └── evaluate.py
│
├── src/                        # Core application logic
│   ├── preprocessing/
│   ├── document_builder/
│   ├── chunking/
│   ├── embeddings/
│   ├── retrieval/
│   ├── llm/
│   ├── evaluation/
│   └── utils/
│
├── tests/                      # Unit and integration tests
│
├── .env.example                # Environment variable template
├── .gitignore
├── Dockerfile
├── pyproject.toml
├── README.md
└── uv.lock
```

---

## Directory Overview

| Directory | Purpose |
|------------|---------|
| **app/** | Contains the Streamlit application that provides the user interface for interacting with the RAG system. |
| **config/** | Stores configuration files, logging configuration, and pipeline settings to keep application behavior configurable without modifying code. |
| **data/** | Central location for all project datasets, including raw data, processed datasets, generated documents, chunks, embeddings, and evaluation data. |
| **docs/** | Contains project documentation, architecture diagrams, design decisions, and supporting materials. |
| **logs/** | Stores application logs generated during preprocessing, indexing, retrieval, and evaluation. |
| **notebooks/** | Used for exploratory data analysis (EDA), experimentation, and prototype development before production implementation. |
| **scripts/** | Provides executable entry points for running different stages of the pipeline without exposing implementation details. |
| **src/** | Contains the core business logic for preprocessing, document construction, chunking, embeddings, retrieval, evaluation, and LLM integration. |
| **tests/** | Includes unit tests and integration tests to validate individual components and the overall pipeline. |

---

## Design Philosophy

The repository is organized around the principle of **separation of concerns**, where each directory has a clearly defined responsibility.

Rather than placing all logic in a single script, the project separates:

- **Configuration** from implementation
- **Data** from application code
- **Pipeline entry points** from business logic
- **Experiments** from production code
- **Documentation** from implementation

This modular organization makes the project easier to maintain, extend, test, and reproduce as new capabilities are added throughout the development of the RAG system.

# Technology Stack

The project leverages modern open-source tools commonly used in AI Engineering and Data Engineering workflows. Each technology has been selected based on simplicity, maintainability, and suitability for building a production-inspired Retrieval-Augmented Generation (RAG) system.

| Layer | Technology | Purpose |
|--------|------------|---------|
| **Programming Language** | Python 3.12+ | Core development language |
| **Package & Environment Management** | uv | Fast dependency management and reproducible environments |
| **Data Processing** | Pandas | Data cleaning, transformation, and preprocessing |
| **Configuration Management** | python-dotenv, YAML | Externalized configuration and environment management |
| **Embedding Model** | BAAI/bge-small-en-v1.5 | Generate dense vector representations for semantic search |
| **Vector Database** | ChromaDB | Store and retrieve vector embeddings efficiently |
| **Large Language Model** | Google Gemini | Generate grounded responses from retrieved context |
| **User Interface** | Streamlit | Interactive web application for natural language querying |
| **Logging** | Python Logging | Structured application logging and debugging |
| **Development Environment** | Jupyter Notebook | Exploratory Data Analysis (EDA) and experimentation |
| **Version Control** | Git & GitHub | Source code management and collaboration |
| **Containerization** | Docker | Portable and reproducible application deployment |

---

## Why These Technologies?

- **Python** provides a rich ecosystem for AI, machine learning, and data engineering.
- **uv** offers fast dependency resolution and reproducible project environments.
- **Pandas** simplifies structured data processing and preprocessing workflows.
- **BAAI/bge-small-en-v1.5** is a lightweight yet high-performing embedding model suitable for semantic retrieval tasks.
- **ChromaDB** is easy to integrate, lightweight, and well-suited for local vector search during development.
- **Google Gemini** provides high-quality natural language generation with strong instruction-following capabilities.
- **Streamlit** enables rapid development of interactive AI applications without extensive frontend development.
- **Docker** ensures the application can be deployed consistently across different environments.

# Engineering Decisions

The project is designed around a set of engineering principles inspired by modern AI Engineering and Data Engineering practices. These decisions prioritize maintainability, modularity, reproducibility, and evaluation over rapid implementation.

---

## 1. Modular Pipeline Architecture

The system is divided into independent pipeline stages, each with a single responsibility.

```text
Raw Data
    ↓
Preprocessing
    ↓
Document Builder
    ↓
Chunking
    ↓
Embeddings
    ↓
Vector Database
    ↓
Retrieval
    ↓
LLM
```

This separation allows each stage to be developed, tested, and improved independently.

---

## 2. Separation of Concerns

Each module is responsible for a single task.

For example:

- **Preprocessing** cleans and normalizes raw data.
- **Document Builder** transforms structured data into retrieval documents.
- **Chunking** prepares documents for embedding.
- **Retriever** performs semantic search.
- **LLM** generates responses using retrieved context.

Keeping responsibilities isolated improves maintainability and reduces coupling between components.

---

## 3. Preserve Business Semantics

Preprocessing intentionally preserves business meaning instead of aggressively transforming the data.

Examples include:

- Keeping **Best Sellers Rank** as text to retain ranking categories.
- Preserving **List Price** labels instead of extracting only numeric values.
- Keeping review text in its natural form without stemming or stop-word removal.

This ensures richer contextual information is available during document construction and retrieval.

---

## 4. Retrieval-Oriented Document Design

The project treats **document modeling** as a dedicated design stage rather than embedding raw CSV rows.

Documents are designed specifically for semantic retrieval by combining structured product information with relevant customer feedback.

This improves retrieval quality and provides richer context to the language model.

---

## 5. Evaluation-Driven Development

Architectural decisions are intended to be validated through evaluation rather than intuition.

Future evaluation will include:

- Retrieval relevance
- Chunking strategy comparison
- Embedding model comparison
- Prompt evaluation
- End-to-end RAG performance

This encourages measurable improvements throughout the project lifecycle.

---

## 6. Configuration-Driven Development

Configuration values are stored outside the application code whenever possible.

Examples include:

- Environment variables
- YAML configuration files
- Logging configuration

This improves flexibility, reproducibility, and maintainability.

---

## 7. Production-Inspired Repository Structure

The repository is organized into independent components for:

- Configuration
- Data
- Source code
- Scripts
- Documentation
- Tests

This mirrors the organization of real-world AI applications and makes the project easier to extend as new features are added.

---

## 8. Reproducibility

The project emphasizes reproducible development through:

- Dependency management with **uv**
- Environment configuration using **.env**
- Version-controlled source code
- Modular pipeline execution
- Deterministic preprocessing workflows

These practices ensure the project can be reliably rebuilt and reproduced across different environments.

# Project Pipeline

The Amazon Product Intelligence Assistant is developed as a sequence of modular pipeline stages, where each component performs a single well-defined responsibility. This design improves maintainability, scalability, and allows each stage to be developed, tested, and evaluated independently.

![Project Pipeline Diagram](docs/architecture/system-architecture.png)

## Pipeline Stages

| Stage | Description |
|--------|-------------|
| **Data Preprocessing** | Cleans and normalizes raw product and review datasets while preserving important business semantics. |
| **Document Modeling** | Defines how structured product information and customer reviews are represented for retrieval. |
| **Document Builder** | Converts processed tabular data into retrieval-optimized textual documents. |
| **Chunking** | Splits documents into semantically meaningful chunks suitable for embedding. |
| **Embedding Generation** | Converts document chunks into dense vector representations. |
| **Vector Database** | Stores embeddings for efficient semantic similarity search. |
| **Semantic Retrieval** | Retrieves the most relevant document chunks based on user queries. |
| **Prompt Construction** | Combines retrieved context with the user's question to create a grounded prompt. |
| **Response Generation** | Uses Google Gemini to generate accurate, context-aware responses grounded in retrieved information. |

# Installation

## Clone the Repository

```bash
git clone https://github.com/<username>/amazon-product-intelligence.git

cd amazon-product-intelligence
```

## Create a Virtual Environment

```bash
uv venv
```

## Activate the Environment

### Windows

```bash
.venv\Scripts\activate
```

### Linux / macOS

```bash
source .venv/bin/activate
```

## Install Dependencies

```bash
uv sync
```

## Configure Environment Variables

Create a `.env` file in the project root.

```env
GEMINI_API_KEY=your_api_key_here
```

Additional configuration options can be managed through the files in the `config/` directory.

# Usage

The project is designed as a modular pipeline where each stage can be executed independently.

## 1. Preprocess the Dataset

```bash
uv run python -m scripts.preprocess_data
```

## 2. Build Retrieval Documents *(Planned)*

```bash
uv run python -m scripts.build_documents
```

## 3. Generate Embeddings *(Planned)*

```bash
uv run python -m scripts.build_embeddings
```

## 4. Launch the Streamlit Application *(Planned)*

```bash
streamlit run app/app.py
```

After launching the application, users will be able to ask natural language questions such as:

- *Does this shirt run true to size?*
- *What quality issues do customers frequently mention?*
- *Compare these two products based on customer reviews.*
- *Is this product worth buying?*

# Evaluation

Evaluation is treated as a core component of the project rather than an afterthought. Every major architectural decision should be supported by measurable improvements instead of intuition.

The project will evaluate both **retrieval quality** and **response quality** throughout development.

## Planned Evaluation Areas

### Retrieval Evaluation

- Top-K Retrieval Accuracy
- Recall@K
- Precision@K
- Context Relevance

### Embedding Evaluation

- Embedding model comparison
- Similarity quality
- Retrieval consistency

### Chunking Evaluation

- Chunk size comparison
- Chunk overlap analysis
- Context preservation

### Prompt Evaluation

- Prompt template comparison
- Context formatting
- Grounding effectiveness

### End-to-End RAG Evaluation

- Answer correctness
- Faithfulness to retrieved context
- Hallucination detection
- Overall response quality

Future iterations of the project will incorporate automated evaluation techniques, including **LLM-as-a-Judge**, to systematically assess generated responses.

# Roadmap

## Phase 1 — Project Foundation

- [x] Repository setup
- [x] Project architecture
- [x] Dataset exploration
- [x] Data preprocessing

---

## Phase 2 — Knowledge Base Construction

- [ ] Document modeling
- [ ] Document builder
- [ ] Chunking strategy
- [ ] Metadata design

---

## Phase 3 — Semantic Search

- [ ] Embedding generation
- [ ] Vector database indexing
- [ ] Semantic retrieval

---

## Phase 4 — Retrieval-Augmented Generation

- [ ] Prompt construction
- [ ] Google Gemini integration
- [ ] End-to-end RAG pipeline

---

## Phase 5 — Evaluation & User Interface

- [ ] Retrieval evaluation
- [ ] Response evaluation
- [ ] Streamlit application
- [ ] Logging & monitoring

---

## Phase 6 — Deployment

- [ ] Docker support
- [ ] Documentation
- [ ] Final project release


# Future Improvements

After completing the MVP, the project can be extended with additional AI Engineering capabilities, including:

## Retrieval

- Hybrid Retrieval (BM25 + Dense Retrieval)
- Cross-Encoder Re-ranking
- Query Expansion
- Query Rewriting

## Knowledge Base

- Multi-document retrieval
- Adaptive chunking
- Metadata-based filtering
- Incremental indexing

## User Experience

- Conversation memory
- Product recommendation workflows
- Interactive product comparison
- Citation highlighting

## Infrastructure

- FastAPI backend
- Cloud deployment
- CI/CD pipeline
- Authentication & authorization
- Monitoring dashboards
- Performance optimization

These enhancements are intentionally postponed to keep the MVP focused, maintainable, and aligned with the learning objectives of the LLM Zoomcamp project.

# References

This project builds upon concepts, methodologies, and tools from the following resources:

## Learning Resources

- LLM Zoomcamp — DataTalks.Club
- LLM Engineering Handbook — Paul Iusztin & Maxime Labonne

## AI & Machine Learning

- Google Gemini API
- Sentence Transformers
- BAAI/bge-small-en-v1.5

## Vector Databases

- ChromaDB

## Data Processing

- Pandas
- NumPy

## Application Development

- Streamlit
- Python
- uv

## Version Control

- Git
- GitHub