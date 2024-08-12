import torch
# from transformers import AutoTokenizer, AutoModelForCausalLM

def generate_one_token_at_a_time(prompt, tokenizer, model, max_length=512):
    if not isinstance(prompt, str):
        prompt = str(prompt)  # 明示的に文字列に変換
    # 初期トークンIDを生成
    token_ids = tokenizer.encode(prompt, add_special_tokens=False, return_tensors="pt")

    # 生成されたトークンIDを保持するリスト
    generated_token_ids = token_ids.tolist()[0]

    # モデルのデバイスにトークンIDを送る
    token_ids = token_ids.to(model.device)

    model.eval()  # モデルを評価モードに設定
    with torch.no_grad():
        for _ in range(max_length):
            # 次のトークンIDを予測
            output = model(token_ids)
            next_token_logits = output.logits[:, -1, :]
            next_token_id = torch.multinomial(torch.nn.functional.softmax(next_token_logits, dim=-1), num_samples=1)
            
            # 終了トークンが生成されたらループを終了
            if next_token_id == tokenizer.eos_token_id:
                break

            # 生成されたトークンIDをリストに追加
            generated_token_ids.append(next_token_id.item())

            # 次の予測のためにトークンIDを更新
            token_ids = torch.cat([token_ids, next_token_id], dim=-1)

            # 生成されたトークンをデコードして出力
            print(tokenizer.decode([next_token_id.item()], skip_special_tokens=True), end='')

    return tokenizer.decode(generated_token_ids, skip_special_tokens=True)

# 使い方例
# prompt = "ここにプロンプトを入力"
# tokenizer, model = loadingLLM()
# output_text = generate_one_token_at_a_time(prompt, tokenizer, model)
# print(output_text)
