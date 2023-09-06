import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from pipeline.comparators import BaseComparator
import faiss


class TFIDFComparator(BaseComparator):
    def compare(self, query_document, documents, num_results=10):
        # Combine title and text to create documents for TF-IDF
        documents_str = documents["title"] + " " + documents["text"]

        # Vectorize the documents using TF-IDF
        tfidf_vectorizer = TfidfVectorizer()
        tfidf_matrix = tfidf_vectorizer.fit_transform(documents_str)

        # Convert TF-IDF matrix to dense vectors for FAISS
        dense_tfidf_matrix = tfidf_matrix.toarray()

        # Build FAISS index
        index = faiss.IndexFlatL2(dense_tfidf_matrix.shape[1])
        index.add(dense_tfidf_matrix)

        # Transform and preprocess the query document
        query_tfidf_vector = tfidf_vectorizer.transform([query_document]).toarray()

        num_results = min(num_results, len(documents_str))

        # Perform similarity search using FAISS
        distances, indices = index.search(query_tfidf_vector, num_results)

        # Retrieve the most similar documents from your DataFrame based on indices
        return documents.iloc[indices[0]]


if __name__ == '__main__':
    test_document = "Coronavirus was first discovered in Wuhan, China in 2019."

    documents = pd.DataFrame(columns=["title", "text"])
    documents.loc[0] = ["Trump", "Trump is the former president of the United States"]
    documents.loc[1] = ["Coronavirus", "Coronavirus is a virus that causes COVID-19"]
    documents.loc[2] = ["Biden", "Biden is the current president of the United States"]

    comparator = TFIDFComparator()
    print(comparator.compare(test_document, documents))
