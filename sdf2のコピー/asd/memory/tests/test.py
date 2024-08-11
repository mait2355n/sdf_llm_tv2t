import gensim
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from gensim.utils import simple_preprocess
import MeCab

m = MeCab.Tagger("-Owakati")

def tokenize_jp(text):
    return m.parse(text).split()

class ConversationDatabase:
    def __init__(self, filename):
        self.filename = filename
        self.model = None
        self.conversations = []

    def add_conversation(self, question, answer):
        self.conversations.append((question, answer))
        with open(self.filename, 'a') as f:
            f.write(f'{question}\t{answer}\n')

    def train_model(self):
        tagged_data = [TaggedDocument(words=tokenize_jp(q), tags=[str(i)]) for i, (q, a) in enumerate(self.conversations)]
        self.model = Doc2Vec(tagged_data, vector_size=20, min_count=1, epochs=100)

    def find_similar_conversations(self, text):
        if not self.model:
            print("Model not trained yet")
            return []
        tokens = tokenize_jp(text)
        vector = self.model.infer_vector(tokens)
        similar_docs = self.model.docvecs.most_similar([vector])
        return [self.conversations[int(i)] for i, _ in similar_docs]

db = ConversationDatabase('conversations.txt')
db.add_conversation('こんにちは', 'こんにちは！')
db.add_conversation('お元気ですか？', 'はい、元気です。')
db.train_model()
print(db.find_similar_conversations('お元気ですか？'))
