from sentence_transformers import SentenceTransformer, util
import spacy
import torch
from pipeline.config import retrieval_model_dir


class EmbeddingExtractor:
    model_name = "paraphrase-MiniLM-L6-v2"
    punctuation = r"""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""

    def __init__(self):
        try:
            self.nlp = spacy.load('en_core_web_sm')
        except OSError:
            import sys
            import subprocess
            python_executable = sys.executable

            command = [python_executable, "-m", "spacy", "download",
                       "en_core_web_sm"]
            subprocess.run(command, check=True)
            self.nlp = spacy.load('en_core_web_sm')

        try:
            self.model = SentenceTransformer(retrieval_model_dir)
        except OSError:
            self.model = SentenceTransformer(self.model_name)
            self.model.save(retrieval_model_dir, self.model_name, True)

    def preprocess(self, text):
        # remove \n\t\r and multiple spaces
        text = ' '.join(text.split()).lower()

        doc = self.nlp(text)

        capitalized_sentence = []

        for token in doc:
            if not (token.text in self.nlp.Defaults.stop_words or token.text in self.punctuation):
                if token.tag_ in ['NNP', 'NNS', 'NNPS']:
                    # Capitalize the token text
                    token_text = token.text.capitalize()
                else:
                    # Add the token as is
                    token_text = token.text
                capitalized_sentence.append(token_text)

        return list(set(capitalized_sentence))

    def get_keywords(self, text, num_keywords=10):
        candidate_keywords = self.preprocess(text)

        # use faiss to retrieve top 5 similar sentences
        corpus_embeddings = self.model.encode(candidate_keywords, convert_to_tensor=True)
        query_embedding = self.model.encode(text, convert_to_tensor=True)

        # We use cosine-similarity and torch.topk to find the highest 5 scores
        cos_scores = util.pytorch_cos_sim(query_embedding, corpus_embeddings)[0]

        # We use torch.topk to find the highest 5 scores
        top_results = torch.topk(cos_scores, k=num_keywords)

        return [candidate_keywords[idx] for idx in top_results[1].tolist()]


if __name__ == '__main__':
    new_text = f"""
    The world has been grappling with the challenges posed by the coronavirus pandemic. From the initial outbreak in Wuhan, China, to its rapid spread across the globe, the virus has led to significant changes in our daily lives. Governments and health organizations have been working tirelessly to contain the virus, implement safety measures, and develop vaccines.

    Social distancing, mask mandates, and lockdowns have become part of the new normal as we strive to curb the virus's transmission. Researchers and medical professionals have been collaborating to better understand the virus's behavior, mutations, and potential long-term effects on health.

    The pandemic has highlighted the importance of global cooperation and scientific advancements. The rapid development and distribution of vaccines have offered hope for a way out of the crisis. However, challenges remain, such as vaccine distribution, addressing vaccine hesitancy, and monitoring the emergence of new variants.

    While we navigate these uncertain times, it's crucial to stay informed through reliable sources, follow recommended guidelines, and support one another. Together, we can overcome the challenges posed by the coronavirus and work towards a healthier and safer future."

    Please note that this text is generated for illustrative purposes and may not reflect the most up-to-date information or accurate details about the coronavirus pandemic. Always refer to trusted sources for accurate and current information.
    """

    exrtactor = EmbeddingExtractor()
    print(exrtactor.get_keywords(new_text))
