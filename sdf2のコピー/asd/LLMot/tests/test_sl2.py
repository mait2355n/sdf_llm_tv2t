import torch
from transformers import LlamaTokenizer, AutoModelForCausalLM

tokenizer = LlamaTokenizer.from_pretrained("novelai/nerdstash-tokenizer-v1", additional_special_tokens=['▁▁'])

model = AutoModelForCausalLM.from_pretrained(
    "stabilityai/japanese-stablelm-instruct-alpha-7b",    
    trust_remote_code=True,
)
model.half()
model.eval()

if torch.cuda.is_available():
    model = model.to("cuda")

def build_prompt(user_query, inputs="", sep="\n\n### "):
    sys_msg = "以下は、タスクを説明する指示と、文脈のある入力の組み合わせです。要求を適切に満たす応答を書きなさい。"
    p = sys_msg
    roles = ["指示", "応答"]
    msgs = [": \n" + user_query, ": "]
    if inputs:
        roles.insert(1, "入力")
        msgs.insert(1, ": \n" + inputs)
    for role, msg in zip(roles, msgs):
        p += sep + role + msg
    return p

# this is for reproducibility.
# feel free to change to get different result
seed = 42
torch.manual_seed(seed)

# Infer with prompt without any additional input
user_inputs = {
    "user_query": "VR とはどのようなものですか？",
    "inputs": ""
}
prompt = build_prompt(**user_inputs)

input_ids = tokenizer.encode(
    prompt, 
    add_special_tokens=False, 
    return_tensors="pt"
)

tokens = model.generate(
    input_ids.to(device=model.device),
    max_new_tokens=256,
    temperature=1,
    top_p=0.95,
    do_sample=True,
)

out = tokenizer.decode(tokens[0][input_ids.shape[1]:], skip_special_tokens=True).strip()
print(out)
"""バーチャルリアリティは、現実の世界のように見える仮想世界の 3D 仮想現実のシミュレーションです。これは、ヘッドセットを介して、ユーザーが見たり、聞いたり、体験できるものです。"""

seed = 42
torch.manual_seed(seed)

# Infer with prompt with additional input
user_inputs = {
    "user_query": "VR について、以下の比較対象との違いを箇条書きで教えてください。",
    "inputs": "比較対象: AR"
}
prompt = build_prompt(**user_inputs)

input_ids = tokenizer.encode(
    prompt, 
    add_special_tokens=False, 
    return_tensors="pt"
)

tokens = model.generate(
    input_ids.to(device=model.device),
    max_new_tokens=256,
    temperature=1,
    top_p=0.95,
    do_sample=True,
)

out = tokenizer.decode(tokens[0][input_ids.shape[1]:], skip_special_tokens=True).strip()
print(out)
"""
以下は、VR と AR の比較対象の比較です。
1. VR はユーザーが3D の世界を体験することを可能にし、ユーザーが自分の目で世界を見ることを可能にします。
2. VR は、ユーザーが目の前の環境をより詳細に感じ、より多くのことができるようにすることを可能にします。
3. VR は、ユーザーの感覚を刺激し、拡張することを可能にします。
4. VR は、視覚的、触覚的、および聴覚的な感覚体験を提供するために使用されます。
5. AR は、現実の世界に重ね合わせて、情報を表示し、ユーザーに拡張現実体験を提供することを可能にします。
6. AR は、ユーザーが仮想オブジェクトを仮想環境に持ち込むことを可能にするため、物理的な世界をシミュレートするのに最適です。
7. VR は、3D 世界を実現する仮想世界を作成することに最適です。
8. AR は、ユーザーが現実世界のオブジェクトをシミュレートし、現実世界の現実的な世界に重ね合わせて情報を表示することを可能にします。
9. VR は、ユーザーの感覚や感情に与える影響が最も大きいと考えられています。
"""
