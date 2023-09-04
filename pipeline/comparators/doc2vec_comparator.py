from gensim.test.utils import common_texts
from gensim.models.doc2vec import Doc2Vec, TaggedDocument

if __name__ == '__main__':
    documents = [TaggedDocument(doc, [i]) for i, doc in enumerate(common_texts)]

    print('\n'.join([str(doc) for doc in documents]))

    model = Doc2Vec(documents, vector_size=5, window=2, min_count=1, workers=4)

    print(model.infer_vector(['system', 'human', 'system', 'eps']))
    print(model.infer_vector(['user', 'response', 'time']))
