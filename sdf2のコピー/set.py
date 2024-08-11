from asd.memory.loading import loadtokenizer
from asd.memory.vec_momory import *

if __name__ == "__main__":
    print("asd")
    model_tokenizer=loadtokenizer()
    #データベースのセッティング
    if not os.path.exists(f"data/vec_mem"):
        os.makedirs(f"data/vec_mem")
        print(f"フォルダ 'data/vec_mem' を作成しました。")
        resped=save_search("自然言語処理は特に何について役に立つ？",1,model_tokenizer,"prompt",k=0)
        save_search("そうだね、この技術はテキスト分析において大変役立つよ。",2,model_tokenizer,"resp",k=0)
        resped=save_search("テキスト分析において役に立つ手法を一つ挙げてほしい",1,model_tokenizer,"prompt",k=1)
        save_search("トピックモデリングはどうかな、大量のテキストデータから隠れたトピックを発見する。LDA（Latent Dirichlet Allocation）などが有名だ。",2,model_tokenizer,"resp",k=1)
        resped=save_search("文埋め込みのベクトルデータベースについて教えてほしい。",1,model_tokenizer,"prompt",k=1)
        save_search("わかった。文埋め込みのベクトルデータベースについて説明するね。これは、文やフレーズを数値ベクトルに変換し、それをデータベースに保存する技術だ。このプロセスは自然言語処理（NLP）において重要で、様々な応用がある。",2,model_tokenizer,"resp",k=1)
        print(resped)
    else:
        resped=save_search("文埋め込みのベクトルデータベースについて教えてほしい。",1,model_tokenizer,"prompt",k=3)
        save_search("わかった。文埋め込みのベクトルデータベースについて説明するね。これは、文やフレーズを数値ベクトルに変換し、それをデータベースに保存する技術だ。このプロセスは自然言語処理（NLP）において重要で、様々な応用がある。",2,model_tokenizer,"resp",k=1)
        print(resped)