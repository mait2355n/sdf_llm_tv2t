import torch
from asd.LLMot.loadingLLM import loadingLLM
from asd.LLMot.LLM import generate_one_token_at_a_time

# テスト関数を定義
def test_generation():
    # モデルとトークナイザーのロード
    device, device1,tokenizer, model = loadingLLM()
    # 生成をテストするプロンプト
    prompt = "ここにプロンプトを入力"
    # 1トークンずつテキストを生成
    generated_text = generate_one_token_at_a_time(prompt, tokenizer, model)
    print(generated_text)

if __name__ == "__main__":
    test_generation()
