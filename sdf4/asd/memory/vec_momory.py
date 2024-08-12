from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import os

# 既存のベクトルデータベース（Faissインデックス）をロードするか、存在しない場合は新しく作成する関数
def load_or_create_index(database_path, model):
    # インデックスファイルが存在するか確認
    if os.path.exists(database_path):
        # 既存のインデックスをロード
        return faiss.read_index(database_path)
    else:
        # 新しいインデックスを作成（モデルからベクトルの次元を取得して使用）
        dimension = model.get_sentence_embedding_dimension()
        return faiss.IndexFlatL2(dimension)

# 既存の文書数を管理するための関数群
def get_existing_docs_count(counter_file):
    # カウンターファイルの存在確認
    if not os.path.exists(counter_file):
        return 0
    with open(counter_file, "r") as file:
        return int(file.read())

def update_document_count(new_count, counter_file):
    with open(counter_file, "w") as file:
        file.write(str(new_count))

# 新しい文書を追加し、それに対応する原文を保存する関数
def add_new_documents(new_sentences, model, index, num, counter_file):
    # new_sentencesが単一の文字列の場合、それを要素とするリストに変換
    if isinstance(new_sentences, str):
        new_sentences = [new_sentences]

    # 現在の文書数をカウンターファイルから取得
    existing_docs_count = get_existing_docs_count(counter_file)

    # 新しい文書のベクトルを生成
    # model.encode() は文書をベクトル化する。これは検索時に文書を識別するのに使用される。ここで用いる文はリスト化する必要がある。
    
    new_embeddings = model.encode(new_sentences)

    # 新しいベクトルをFaissインデックスに追加
    # Faissは高速な検索のために文書のベクトルを効率的に格納する。
    index.add(np.array(new_embeddings))
    if not os.path.exists(f"data/vec_mem/{num}"):
        os.makedirs(f"data/vec_mem/{num}")
        print(f"フォルダ 'data/vec_mem/{num}' を作成しました。")
    # 新しい文書の原文を個別のファイルとして保存
    # 各ファイル名は 'document_{ID}.txt' の形式で、IDはその文書の一意の識別子。
    for i, sentence in enumerate(new_sentences):
        file_name = f"data/vec_mem/{num}/document_{existing_docs_count + i}.txt"
        with open(file_name, "w") as file:
            file.write(sentence)

    # 文書数を更新し、新しいカウントをカウンターファイルに保存
    update_document_count(existing_docs_count + len(new_sentences), counter_file)

# クエリに基づいて検索を行い、対応する原文を取得する関数
def search_and_retrieve_original_text(query, model, index, num, k):
    # クエリをベクトル化
    # 入力されたクエリテキストをベクトルに変換し、これを検索のために使用する。
    query_embedding = model.encode([query])

    # Faissインデックスを用いて検索を実行
    # クエリベクトルに最も近いベクトル（文書）をFaissインデックスから探す。
    if k!=0:
        distances, indices = index.search(np.array(query_embedding), k)
    else:
        indices=[]
    '''
    # 検索結果のインデックスに対応する文書の原文を取得
    original_texts = []
    for idx in indices[0]:
        # 各インデックスに対応するファイル名を生成し、ファイルが存在する場合はその内容を読み込む。
        file_name = f"data/vec_mem/{num}/doc_a_all/document_{idx}.txt"
        if os.path.exists(file_name):
            with open(file_name, "r") as file:
                original_text = file.read()
                original_texts.append(original_text)
    '''
    return indices

def save_search(sentence,num,model,database_name,k):
    database_path=f"data/vec_mem/{database_name}.idx"
    index = load_or_create_index(database_path, model)
    # インデックスを保存（更新後）
    faiss.write_index(index, f"data/vec_mem/{database_name}.idx")
    
    if num == 1:
        i=0
        # 今回のプロンプトの保存（サンプル）
        add_new_documents(sentence, model, index, num, f"data/vec_mem/docount_{database_name}.txt")
        #検索クエリの実行例/memoryはリスト型
        indices = search_and_retrieve_original_text(sentence, model, index, num,k)
        # 検索結果のインデックスに対応する文書の原文を取得
        original_texts = [[],[],[]],[[],[],[]]
        for idx in indices[0]:
            # 各インデックスに対応するファイル名を生成し、ファイルが存在する場合はその内容を読み込む。
            file_name = f"data/vec_mem/1/document_{idx}.txt"
            
            if os.path.exists(file_name):
                with open(file_name, "r") as file:
                    original_text = file.read()
                    original_texts[0][i]+=[original_text]
            file_name = f"data/vec_mem/2/document_{idx}.txt"
            
            if os.path.exists(file_name):
                with open(file_name, "r") as file:
                    original_text = file.read()
                    original_texts[1][i]+=[original_text]
            i+=1
        print(original_texts)
        
        return original_texts
    return 
    
    
#num=1の時、入力プロンプトを表す。
#num=2の時、LLMからの回答分を表す。