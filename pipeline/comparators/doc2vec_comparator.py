import gensim
from gensim.utils import simple_preprocess
from gensim.parsing.preprocessing import remove_stopwords
from gensim.models.doc2vec import TaggedDocument
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from pipeline.comparators import BaseComparator


class Doc2VecComparator(BaseComparator):

    def preprocess_document(self, document):
        # Tokenize and remove stopwords
        tokens = simple_preprocess(remove_stopwords(document))
        return tokens

    def compare(self, query_document, documents, num_results=10):
        documents_str = documents["title"] + " " + documents["text"]

        # convert to list of tokens
        listed_documents = [self.preprocess_document(doc) for doc in documents_str]

        tagged_data = [TaggedDocument(words=doc, tags=[str(i)]) for i, doc in enumerate(listed_documents)]

        vector_size = 100  # Adjust as needed
        window = 5
        min_count = 2
        workers = 4
        epochs = 50

        model = gensim.models.Doc2Vec(vector_size=vector_size, window=window, min_count=min_count, workers=workers)
        model.build_vocab(tagged_data)
        model.train(tagged_data, total_examples=model.corpus_count, epochs=epochs)
        preprocessed_new_doc = self.preprocess_document(query_document)

        document_vectors = [model.infer_vector(doc) for doc in listed_documents]
        query_vector = model.infer_vector(preprocessed_new_doc)

        # Perform similarity search using FAISS
        similarities = cosine_similarity([query_vector], document_vectors)[0]

        # Get the indices of documents sorted in descending order of similarity
        sorted_indices = np.argsort(similarities)[::-1]

        # Determine the number of results to return
        num_results = min(num_results, len(listed_documents))

        # Get the top "num_results" most similar documents
        return documents.iloc[sorted_indices[:num_results]]


if __name__ == '__main__':
    import pandas as pd

    test_document = "Coronavirus was first discovered in Wuhan, China in 2019."

    documents = pd.DataFrame(columns=["title", "text"])
    documents.loc[0] = ["Trump", "Trump is the former president of the United States"]
    documents.loc[1] = ["Coronavirus", "Coronavirus is a virus that causes COVID-19"]
    documents.loc[2] = ["Biden", "Biden is the current president of the United States"]

    comparator = Doc2VecComparator()
    print(comparator.compare(test_document, documents))
