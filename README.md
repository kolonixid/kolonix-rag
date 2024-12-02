# Example usage
```
if __name__ == "__main__":
    mongo_url = 'your_mongo_url_here'
    db_name = 'chat-service'
    collection_name = 'rag'
    model_name = 'sentence-transformers/all-MiniLM-L6-v2'
    similarity_threshold = 0.3

    rag = RAGFramework(mongo_url, db_name, collection_name, model_name, similarity_threshold)

    # Update embeddings for existing documents
    rag.update_embeddings()

    # Insert new data
    raw_text = "This is a sample document text that needs to be inserted into MongoDB."
    result = rag.insert_data(raw_text)
    print(result)

    # Retrieve data based on a query
    query = "sample document text"
    retrieved_data = rag.retrieve_data(query)
    print(retrieved_data)
```