import numpy as np
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from string import punctuation


class SpacyKeywordExtractor:

    def __init__(self):
        self.nlp = spacy.load('en_core_web_sm')
        self.tfidf_vectorizer = TfidfVectorizer()

    def get_keywords(self, text, num_keywords=10):
        result = []
        pos_tag = ['NOUN']
        doc = self.nlp(text.lower())
        for token in doc:
            if token.text in self.nlp.Defaults.stop_words or token.text in punctuation:
                continue
            if token.pos_ in pos_tag:
                result.append(token.text)
        keyword_text = ' '.join(result)

        # Fit and transform the TF-IDF vectorizer
        tfidf_matrix = self.tfidf_vectorizer.fit_transform([keyword_text])

        # Get the TF-IDF feature names
        feature_names = self.tfidf_vectorizer.get_feature_names_out()

        tfidf_sums = np.array(tfidf_matrix.sum(axis=0)).flatten()

        # Get the indices of the words with highest TF-IDF sums
        top_indices = tfidf_sums.argsort()[-num_keywords:][::-1]

        # Get the top keywords based on the indices
        top_keywords = [feature_names[idx] for idx in top_indices]

        return top_keywords


if __name__ == '__main__':
    new_text = f"""
    The world has been grappling with the challenges posed by the coronavirus pandemic. From the initial outbreak in Wuhan, China, to its rapid spread across the globe, the virus has led to significant changes in our daily lives. Governments and health organizations have been working tirelessly to contain the virus, implement safety measures, and develop vaccines.

    Social distancing, mask mandates, and lockdowns have become part of the new normal as we strive to curb the virus's transmission. Researchers and medical professionals have been collaborating to better understand the virus's behavior, mutations, and potential long-term effects on health.

    The pandemic has highlighted the importance of global cooperation and scientific advancements. The rapid development and distribution of vaccines have offered hope for a way out of the crisis. However, challenges remain, such as vaccine distribution, addressing vaccine hesitancy, and monitoring the emergence of new variants.

    While we navigate these uncertain times, it's crucial to stay informed through reliable sources, follow recommended guidelines, and support one another. Together, we can overcome the challenges posed by the coronavirus and work towards a healthier and safer future."

    Please note that this text is generated for illustrative purposes and may not reflect the most up-to-date information or accurate details about the coronavirus pandemic. Always refer to trusted sources for accurate and current information.
    """

    extractor = SpacyKeywordExtractor()
    print(extractor.get_keywords(new_text))
