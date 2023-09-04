from sklearn.feature_extraction.text import TfidfVectorizer
import faiss


class TFIDFComparator:
    def compare(self, query_document, documents, num_results=10):
        # Combine title and text to create documents for TF-IDF
        documents = documents["title"] + " " + documents["text"]

        # Vectorize the documents using TF-IDF
        tfidf_vectorizer = TfidfVectorizer()
        tfidf_matrix = tfidf_vectorizer.fit_transform(documents)

        # Convert TF-IDF matrix to dense vectors for FAISS
        dense_tfidf_matrix = tfidf_matrix.toarray()

        # Build FAISS index
        index = faiss.IndexFlatL2(dense_tfidf_matrix.shape[1])
        index.add(dense_tfidf_matrix)

        # Transform and preprocess the query document
        query_tfidf_vector = tfidf_vectorizer.transform([query_document]).toarray()

        num_results = min(num_results, len(documents))

        # Perform similarity search using FAISS
        distances, indices = index.search(query_tfidf_vector, num_results)

        # Retrieve the most similar documents from your DataFrame based on indices
        return documents.iloc[indices[0]]


if __name__ == '__main__':
    test_document = f"""
The world has been grappling with the challenges posed by the coronavirus pandemic. From the initial outbreak in Wuhan, China, to its rapid spread across the globe, the virus has led to significant changes in our daily lives. Governments and health organizations have been working tirelessly to contain the virus, implement safety measures, and develop vaccines.

Social distancing, mask mandates, and lockdowns have become part of the new normal as we strive to curb the virus's transmission. Researchers and medical professionals have been collaborating to better understand the virus's behavior, mutations, and potential long-term effects on health.

The pandemic has highlighted the importance of global cooperation and scientific advancements. The rapid development and distribution of vaccines have offered hope for a way out of the crisis. However, challenges remain, such as vaccine distribution, addressing vaccine hesitancy, and monitoring the emergence of new variants.

While we navigate these uncertain times, it's crucial to stay informed through reliable sources, follow recommended guidelines, and support one another. Together, we can overcome the challenges posed by the coronavirus and work towards a healthier and safer future."

Please note that this text is generated for illustrative purposes and may not reflect the most up-to-date information or accurate details about the coronavirus pandemic. Always refer to trusted sources for accurate and current information.
"""
    from pipeline.scrapers import Scraper

    documents = Scraper().search("coronavirus", top_n=10)
    comparator = TFIDFComparator()
    print(comparator.compare(test_document, documents))
