from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import os

# 既存のベクトルデータベース（Faissインデックス）をロードする
index = faiss.read_index("sentence_index.idx")  # 既存のインデックスのパス

# モデルのロード
model = SentenceTransformer('nlp-waseda/roberta-base-japanese')

# 新しい文書の追加
new_sentences = ["新しい文書1", "新しい文書2"]
new_embeddings = model.encode(new_sentences)
index.add(np.array(new_embeddings))

# 新しい文書の原文を保存
existing_docs_count = 100  # 既存の文書数（これに基づいて新しいIDを割り当てる）
for i, sentence in enumerate(new_sentences):
    file_name = f"document_{existing_docs_count + i}.txt"
    with open(file_name, "w") as file:
        file.write(sentence)

# インデックスを保存（更新後）
faiss.write_index(index, "path_to_existing_index.faiss")

def search_and_retrieve_original_text(query, model, index, k=1):
    # クエリをベクトル化
    query_embedding = model.encode([query])
    
    # Faissで検索
    distances, indices = index.search(np.array(query_embedding), k)
    
    # 対応する原文の取得
    original_texts = []
    for idx in indices[0]:
        file_name = f"document_{idx}.txt"
        if os.path.exists(file_name):
            with open(file_name, "r") as file:
                original_text = file.read()
                original_texts.append(original_text)
    
    return original_texts

# 検索クエリ
query = "検索したい内容"

# 検索と原文の取得
original_texts = search_and_retrieve_original_text(query, model, index)
for text in original_texts:
    print("asdasd#####",text)
  