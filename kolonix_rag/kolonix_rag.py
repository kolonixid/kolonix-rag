import pymongo
from sentence_transformers import SentenceTransformer
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import numpy as np
import string


class RAGFramework:
    def __init__(self, mongo_url, db_name, collection_name, model_name='sentence-transformers/all-MiniLM-L6-v2',
                 similarity_threshold=0.3):
        self.mongo_client = pymongo.MongoClient(mongo_url)
        self.db = self.mongo_client[db_name]
        self.collection = self.db[collection_name]
        self.model_sentence = SentenceTransformer(model_name)
        self.similarity_threshold = similarity_threshold
        try:
            nltk.data.find('corpora/punkt_tab')
        except LookupError:
            nltk.download('punkt_tab')
        # Download NLTK stopwords
        try:
            nltk.data.find('corpora/stopwords')
        except LookupError:
            nltk.download('stopwords')

        self.stop_words = set(stopwords.words('english'))

    def update_embeddings(self):
        for doc in self.collection.find():
            if 'embedding' not in doc:
                embedding = self.model_sentence.encode(doc['doc'])
                self.collection.update_one({'_id': doc['_id']}, {'$set': {'embedding': embedding.tolist()}})

    def insert_data(self, raw_text):
        try:
            document = {"doc": raw_text}
            embedding = self.model_sentence.encode(document['doc'])
            last_docs = {"doc": document['doc'], "embedding": embedding.tolist()}
            self.collection.insert_one(last_docs)
            return "Data inserted successfully."
        except Exception as e:
            return f"Error inserting data: {e}"

    def extract_keywords(self, query):
        tokens = word_tokenize(query.lower())
        keywords = [word for word in tokens if word not in self.stop_words and word not in string.punctuation]
        return keywords

    def retrieve_data(self, raw_query):
        print("Retrieving data...: " + raw_query)
        try:
            keywords = self.extract_keywords(raw_query)
            text_query = " ".join(keywords)
            query_embedding = self.model_sentence.encode(text_query)
            results = []
            for doc in self.collection.find():
                doc_embedding = np.array(doc['embedding'])
                similarity = np.dot(query_embedding, doc_embedding) / (
                            np.linalg.norm(query_embedding) * np.linalg.norm(doc_embedding))
                if similarity > self.similarity_threshold:
                    results.append(doc["doc"])
            print(results)
            return results
        except Exception as e:
            return f"Error retrieving data: {e}"

    def load_context(self, file_path):
        with open(file_path, 'r') as file:
            return file.read()

    def save_context(self, file_path, content):
        with open(file_path, 'w') as file:
            file.write(content)


# Example usage
# if __name__ == "__main__":
#     mongo_url = 'mongodb://localhost:27017/'
#     db_name = 'chat-service'
#     collection_name = 'rag'
#     model_name = 'sentence-transformers/all-MiniLM-L6-v2'
#     similarity_threshold = 0.3
#
#     rag = RAGFramework(mongo_url, db_name, collection_name, model_name, similarity_threshold)
#
#     # Update embeddings for existing documents
#     rag.update_embeddings()
#
#     # Insert new data
#     raw_text = "This is a sample document text that needs to be inserted into MongoDB."
#     result = rag.insert_data(raw_text)
#     print(result)
#
#     # Retrieve data based on a query
#     query = "sample document text"
#     retrieved_data = rag.retrieve_data(query)
#     print(retrieved_data)