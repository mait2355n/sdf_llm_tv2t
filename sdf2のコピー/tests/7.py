from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import os

# モデルのロード
model = SentenceTransformer('nlp-waseda/roberta-base-japanese')

# 既存のベクトルデータベース（Faissインデックス）をロード、または新しいインデックスを作成
def load_or_create_index(path_to_index, model):
    if os.path.exists(path_to_index):
        return faiss.read_index(path_to_index)
    else:
        dimension = model.get_sentence_embedding_dimension()
        return faiss.IndexFlatL2(dimension)

index = load_or_create_index("path_to_existing_index.faiss", model)

# 文書数を管理するための関数
def get_existing_docs_count(file_path="document_count.txt"):
    if not os.path.exists(file_path):
        return 0
    with open(file_path, "r") as file:
        return int(file.read())

def update_document_count(new_count, file_path="document_count.txt"):
    with open(file_path, "w") as file:
        file.write(str(new_count))

# 新しい文書を追加する関数
def add_new_documents(new_sentences, model, index, counter_file="document_count.txt"):
    existing_docs_count = get_existing_docs_count(counter_file)
    new_embeddings = model.encode(new_sentences)
    index.add(np.array(new_embeddings))

    for i, sentence in enumerate(new_sentences):
        file_name = f"document_{existing_docs_count + i}.txt"
        with open(file_name, "w") as file:
            file.write(sentence)

    update_document_count(existing_docs_count + len(new_sentences), counter_file)

# インデックスを保存（更新後）
faiss.write_index(index, "path_to_existing_index.faiss")

# 新しい文書の追加例
new_sentences = ["新しい文書1", "新しい文書2"]
add_new_documents(new_sentences, model, index)

# 検索関数
def search_and_retrieve_original_text(query, model, index, k=1):
    query_embedding = model.encode([query])
    distances, indices = index.search(np.array(query_embedding), k)
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
    print(text)
