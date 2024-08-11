from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import os

# モデルのロード（文書をベクトル化するためのモデル）
model = SentenceTransformer('nlp-waseda/roberta-base-japanese')

# 既存のベクトルデータベース（Faissインデックス）をロードするか、存在しない場合は新しく作成する関数
def load_or_create_index(path_to_index, model):
    # インデックスファイルが存在するか確認
    if os.path.exists(path_to_index):
        # 既存のインデックスをロード
        return faiss.read_index(path_to_index)
    else:
        # 新しいインデックスを作成（モデルからベクトルの次元を取得して使用）
        dimension = model.get_sentence_embedding_dimension()
        return faiss.IndexFlatL2(dimension)

# インデックスのロード（または新規作成）
index = load_or_create_index("data/vec_mem/1/sentind.idx", model)

# 既存の文書数を管理するための関数群
def get_existing_docs_count(file_path="data/vec_mem/1/docount.txt"):
    # カウンターファイルの存在確認
    if not os.path.exists(file_path):
        return 0
    with open(file_path, "r") as file:
        return int(file.read())

def update_document_count(new_count, file_path="data/vec_mem/1/docount.txt"):
    with open(file_path, "w") as file:
        file.write(str(new_count))

# 新しい文書を追加し、それに対応する原文を保存する関数
def add_new_documents(new_sentences, model, index, counter_file="data/vec_mem/1/docount.txt"):
    # 現在の文書数をカウンターファイルから取得
    existing_docs_count = get_existing_docs_count(counter_file)

    # 新しい文書のベクトルを生成
    # model.encode() は文書をベクトル化する。これは検索時に文書を識別するのに使用される。
    new_embeddings = model.encode(new_sentences)

    # 新しいベクトルをFaissインデックスに追加
    # Faissは高速な検索のために文書のベクトルを効率的に格納する。
    index.add(np.array(new_embeddings))

    # 新しい文書の原文を個別のファイルとして保存
    # 各ファイル名は 'document_{ID}.txt' の形式で、IDはその文書の一意の識別子。
    for i, sentence in enumerate(new_sentences):
        file_name = f"data/vec_mem/1/doc_all/document_{existing_docs_count + i}.txt"
        with open(file_name, "w") as file:
            file.write(sentence)

    # 文書数を更新し、新しいカウントをカウンターファイルに保存
    update_document_count(existing_docs_count + len(new_sentences), counter_file)

# インデックスを保存（更新後）
faiss.write_index(index, "data/vec_mem/sentind.idx")

# 新しい文書の追加（サンプル）
new_sentences = ["新しい文書1", "新しい文書2"]
add_new_documents(new_sentences, model, index)

# クエリに基づいて検索を行い、対応する原文を取得する関数
def search_and_retrieve_original_text(query, model, index, k=1):
    # クエリをベクトル化
    # 入力されたクエリテキストをベクトルに変換し、これを検索のために使用する。
    query_embedding = model.encode([query])

    # Faissインデックスを用いて検索を実行
    # クエリベクトルに最も近いベクトル（文書）をFaissインデックスから探す。
    distances, indices = index.search(np.array(query_embedding), k)

    # 検索結果のインデックスに対応する文書の原文を取得
    original_texts = []
    for idx in indices[0]:
        # 各インデックスに対応するファイル名を生成し、ファイルが存在する場合はその内容を読み込む。
        file_name = f"data/vec_mem/1/doc_all/document_{idx}.txt"
        if os.path.exists(file_name):
            with open(file_name, "r") as file:
                original_text = file.read()
                original_texts.append(original_text)
    return original_texts

#検索クエリの実行例
query = "検索したい内容"
original_texts = search_and_retrieve_original_text(query, model, index)

#検索結果の表示
for text in original_texts:
    print(text)