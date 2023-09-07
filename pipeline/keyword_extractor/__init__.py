from abc import abstractmethod


class Extractor:
    @abstractmethod
    def get_keywords(self, text, num_keywords=10):
        pass


from pipeline.keyword_extractor.embedding_extractor import EmbeddingExtractor
from pipeline.keyword_extractor.chatgpt_extractor import ChatGPTExtractor
from pipeline.keyword_extractor.spacy_extractor import SpacyExtractor
