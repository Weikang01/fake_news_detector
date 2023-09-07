from abc import abstractmethod


class BaseComparator:

    @abstractmethod
    def compare(self, query_document, documents, num_results=10):
        pass


from pipeline.comparators.doc2vec_comparator import Doc2VecComparator
from pipeline.comparators.tfidf_comparator import TFIDFComparator
from pipeline.comparators.embedding_comparator import EmbeddingComparator
