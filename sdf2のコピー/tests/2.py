from sentence_transformers import SentenceTransformer
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# モデルのロード
model = SentenceTransformer('all-MiniLM-L6-v2')

# 2つの文
sentence1 = "この技術はテキスト分析で大変役立つ。"
sentence2 = "この技術は、大量のテキストデータを扱う際に特に有用で、文の意味を迅速に理解し、関連する情報を見つけ出すのに役立つ。"

# 文のベクトル化
embedding1 = model.encode(sentence1)
embedding2 = model.encode(sentence2)
print("a")
# コサイン類似度の計算
cosine_sim = cosine_similarity([embedding1], [embedding2])

print("コサイン類似度:", cosine_sim[0][0])
