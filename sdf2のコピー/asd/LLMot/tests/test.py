import torch
from transformers import LlamaTokenizer, AutoModelForCausalLM

tokenizer = LlamaTokenizer.from_pretrained("novelai/nerdstash-tokenizer-v1", additional_special_tokens=['<NL>'])

model = AutoModelForCausalLM.from_pretrained(
    "stabilityai/japanese-stablelm-base-alpha-7b",
    torch_dtype=torch.float32,
    trust_remote_code=True,
)


if torch.cuda.is_available():
    model = model.to("mps")

prompt = """
[
現在年月日時
<NL>2023-08-11 10:37:41.738575
前提知識
<NL>名前:フルル・リグバート
<NL>目的:世界中の本を読むこと
<NL>現在可能なこと:小説が書ける
関連会話
<NL>mait:こんにちは
<NL>フルル:こんにちは！今日はいい日ですね。
<NL>mait:やあ
<NL>フルル:どうしました？
<NL>mait:そうだな
<NL>フルル:どうしたんですか？
会話履歴
<NL>mait:こんにちは
<NL>フルル:こんにちは！今日はいい日ですね。
<NL>mait:やあ
<NL>フルル:どうしました？
<NL>mait:そうだな
<NL>フルル:どうしたんですか？
今回のプロンプト
<NL>mait:こんにちは。では君の名前と目的、それと現在可能なことを踏まえて自己紹介してほしい。
<NL>フルル:
"""

token_ids = tokenizer.encode(
    prompt,
    add_special_tokens=False,
    return_tensors="pt"
)

# this is for reproducibility.
# feel free to change to get different result
seed = 23  
torch.manual_seed(seed)

output_ids = model.generate(
            token_ids.to(model.device),
            do_sample=True,
            max_new_tokens=128,
            temperature=0.7,
            repetition_penalty=0.95,
            pad_token_id=tokenizer.pad_token_id,
            bos_token_id=tokenizer.bos_token_id,
            eos_token_id=tokenizer.eos_token_id
)

out = tokenizer.decode(output_ids.tolist()[0][token_ids.size(1):])
print(out)
"""
AI で科学研究を加速するには、データ駆動型文化が必要であることも明らかになってきています。研究のあらゆる側面で、データがより重要になっているのです。
20 世紀の科学は、研究者が直接研究を行うことで、研究データを活用してきました。その後、多くの科学分野ではデータは手動で分析されるようになったものの、これらの方法には多大なコストと労力がかかることが分かりました。 そこで、多くの研究者や研究者グループは、より効率的な手法を開発し、研究の規模を拡大してきました。21 世紀になると、研究者が手動で実施する必要のある研究は、その大部分を研究者が自動化できるようになりました。
"""