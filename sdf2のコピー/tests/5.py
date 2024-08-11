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
    print(f"文：{sentences[indices[0][i]]} \n類似度スコア（距離の逆数）：{1 / (1 + distances[0][i])}")