from sentence_transformers import SentenceTransformer, util
from pipeline.comparators import BaseComparator
from pipeline.config import retrieval_model_dir


class EmbeddingComparator(BaseComparator):
    model_name = "paraphrase-MiniLM-L6-v2"

    def __init__(self):
        try:
            self.model = SentenceTransformer(retrieval_model_dir)
        except OSError:
            self.model = SentenceTransformer(self.model_name)
            self.model.save(retrieval_model_dir, self.model_name, True)

    def compare(self, query_document, documents, num_results=10):
        # Compute embedding for both lists
        query_embedding = self.model.encode(query_document, convert_to_tensor=True)
        document_embeddings = self.model.encode(documents["text"].tolist(), convert_to_tensor=True)

        # Compute cosine-similarities
        cosine_scores = util.pytorch_cos_sim(query_embedding, document_embeddings)[0]
        # print(cosine_scores)

        # Output the pairs with their score
        results = []
        for i in range(len(cosine_scores)):
            results.append({"score": cosine_scores[i], "index": i})

        # Sort in decreasing order of relevance
        results = sorted(results, key=lambda x: x["score"], reverse=True)

        # Get the top "num_results" most similar documents
        return documents.iloc[[result["index"] for result in results[:num_results]]]


if __name__ == '__main__':
    import pandas as pd

    test_document = "Coronavirus was first discovered in Wuhan, China in 2019."

    documents = pd.DataFrame(columns=["title", "text"])
    documents.loc[0] = ["Trump", "Trump is the former president of the United States"]
    documents.loc[1] = ["Coronavirus", "Coronavirus is a virus that causes COVID-19"]
    documents.loc[2] = ["Biden", "Biden is the current president of the United States"]

    comparator = EmbeddingComparator()
    print(comparator.compare(test_document, documents))
