from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# モデルのロード
model = SentenceTransformer('nlp-waseda/roberta-base-japanese')

# ベクトルデータベースの準備
dimension = model.get_sentence_embedding_dimension()
index = faiss.IndexFlatL2(dimension)

# 文のベクトル化とデータベースへの追加
sentences = ["この技術はテキスト分析において大変役立つ。", "この方法は非常に有用だ。", "別のトピックについて話す。", "この技術は、大量のテキストデータを扱う際に特に有用で、文の意味を迅速に理解し、関連する情報を見つけ出すのに役立つ。"]
embeddings = model.encode(sentences)
index.add(np.array(embeddings))

# インデックスをファイルに保存
faiss.write_index(index, 'sentence_index.idx')

# 保存したインデックスを読み込む
loaded_index = faiss.read_index('sentence_index.idx')

# 類似度検索を行う文
query = "このテキスト分析技術は非常に役に立つ。"
query_embedding = model.encode(query)

# 類似度検索の実行
k = 3  # 最も類似している文の数
distances, indices = loaded_index.search(np.array([query_embedding]), k)

# 結果の表示
print("検索結果：")
for i in range(k):
    print(f"文：{sentences[indices[0][i]]} \n類似度スコア（距離の逆数）：{1 / (1 + distances[0][i])}")

# 新しい文
new_sentences = ["これはその有用な方法の1つだ。", "この方法は役に立たない。"]

# 新しい文のベクトル化
new_embeddings = model.encode(new_sentences)

# 既存のFaissインデックスをロード（もし保存されている場合）
index = faiss.read_index('sentence_index.idx')

# 新しいベクトルをインデックスに追加
index.add(new_embeddings)

# インデックスの保存
faiss.write_index(index, 'sentence_index.idx')

# インデックスを読み込む
loaded_index = faiss.read_index('sentence_index.idx')

# 類似度検索を行う文
query = "このテキスト分析技術は非常に役に立つ。"
query_embedding = model.encode(query)

# 類似度検索の実行
k = 3  # 最も類似している文の数
distances, indices = loaded_index.search(np.array([query_embedding]), k)

# 結果の表示
print("検索結果：")
for i in range(k):
    print(f"文：{sentences[indices[0][0]]} \n類似度スコア（距離の逆数）：{1 / (1 + distances[0][i])}")