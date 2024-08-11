from sentence_transformers import SentenceTransformer
import faiss

# モデルのロード
model = SentenceTransformer('nlp-waseda/roberta-base-japanese')  # ここに使用するモデル名を入力

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
