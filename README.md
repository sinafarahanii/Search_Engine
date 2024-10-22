
# Information Retrieval Project

## Overview

This project focuses on **information retrieval** using index construction and query processing techniques. The main objective is to create an efficient **positional index** to store document data and handle queries, retrieving relevant documents based on term frequencies and positions.

## Features

- **Positional Index Construction**: 
  - The project iterates through documents, tokenizes them, and normalizes their content using the `normalize` function.
  - Tokens are stemmed using the `Parsivar` library to handle inflections, storing the root form in the index.
  - The index structure stores:
    ```
    {term: [document frequency, {DocID: [term frequency, [positions]]}]}
    ```

- **Common Term Elimination**:
  - After constructing the index, the most frequent 50 terms are eliminated to reduce noise, including common words like "the", "and", etc.

- **TF-IDF Calculation**:
  - Once the index is built, the **TF-IDF** (Term Frequency-Inverse Document Frequency) weight for each term in a document is computed.
  - Example format:
    ```
    'example_term': {'DocID': [TF-IDF weight, [positions]]}
    ```

- **Document Length Calculation**:
  - A `doc_length` dictionary is created by calculating the Euclidean norm of the TF-IDF weights in each document to normalize document scores during query processing.

- **Champion List Creation**:
  - A **Champion List** is constructed for efficient query processing by sorting documents based on term frequency and selecting the top-scoring ones.

- **Query Processing**:
  - Queries are tokenized, normalized, and processed to find the most relevant documents using the **Champion List**.
  - The similarity between query terms and documents is computed based on their TF-IDF scores, returning the top 10 matching documents.

## How it Works

1. **Index Construction**:
   - Documents are tokenized, normalized, and indexed.
   - A positional index is created to track the occurrences and positions of terms in each document.
   - The top 50 most common terms are filtered out to improve search accuracy.

2. **Query Processing**:
   - The system processes incoming queries by normalizing and tokenizing the input.
   - It retrieves documents based on the similarity between the query terms and the documents in the index, ranked using their TF-IDF scores.

3. **Result Retrieval**:
   - The top-ranked documents are displayed based on their relevance to the input query.

## Example Queries

- A single-word query (e.g., "independence") returns relevant documents ranked by their relevance scores.
- Multi-word queries (e.g., "budget plan") are processed similarly, with results sorted by relevance.

## Tools and Libraries

- **Python**: Main programming language for the project.
- **Parsivar**: A Persian NLP library used for tokenization and stemming.
- **TF-IDF**: For term weighting and relevance scoring.
- **Champion List**: For efficient query matching.

## Future Improvements

- **Performance Optimization**: Enhance the indexing and query processing time for large datasets.
- **Advanced Query Handling**: Support more complex queries (e.g., boolean, phrase searches).
- **Language Support**: Extend the system to handle multiple languages and improve stemming techniques.

---

### Author
- **Sina Farahani**
