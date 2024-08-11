from sentence_transformers import SentenceTransformer
import numpy as np

# 使用するモデルを選択（例：'all-MiniLM-L6-v2'）
model = SentenceTransformer('all-MiniLM-L6-v2')

# 例文
sentence = "この技術は、大量のテキストデータを扱う際に特に有用で、文の意味を迅速に理解し、関連する情報を見つけ出すのに役立つ。"

# 文のベクトル化
sentence_embedding = model.encode(sentence)

# ベクトルの表示（最初の5要素のみ表示）
print(sentence_embedding[:])