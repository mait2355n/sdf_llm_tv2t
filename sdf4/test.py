import torch
from asd.LLMot.loadingLLM import loadingLLM
from asd.LLMot.LLM import generate_one_token_at_a_time

# テスト関数を定義
def test_generation():
    # モデルとトークナイザーのロード
    device, device1,tokenizer, model = loadingLLM()
    # 生成をテストするプロンプト
    prompt = [
        {"role": "system", "content": "以下は、タスクを説明する指示と、文脈のある入力の組み合わせです。要求を適切に満たす応答を書きなさい。また、タスク終了時、ＡＡＡＡと出力しなさい"},
        {"role": "user", "name": "mait","content": "たぬきってどういう動物だ？"},
    ]
    # 1トークンずつテキストを生成
    generated_text = generate_one_token_at_a_time(prompt, tokenizer, model)
    print(generated_text)

if __name__ == "__main__":
    test_generation()
