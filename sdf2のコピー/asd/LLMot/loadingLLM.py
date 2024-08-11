import platform
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

def loadingLLM():
  #デバイス情報を取得
  dfg=platform.machine()
  #GPU情報を割り当て,LLMの読み込み
  print("LLM読み込み開始。")
  if dfg=='arm64':
    device='mps'
    device1='cpu'
    tokenizer = AutoTokenizer.from_pretrained(
      "data/models/tokyotech-llmSwallow-MS-7b-v0.1", 
      #"rinna/japanese-gpt-neox-3.6b-instruction-ppo", 
      use_fast=False,
    )
    model = AutoModelForCausalLM.from_pretrained(
      "data/models/tokyotech-llmSwallow-MS-7b-v0.1", 
      #"rinna/japanese-gpt-neox-3.6b-instruction-ppo", 
      #load_in_8bit=True,
      torch_dtype=torch.float32,
      #device_map="auto",
      trust_remote_code=True
    )
  elif dfg=='AMD64':
    device="cuda:0"
    device1="cuda:0"
    tokenizer = AutoTokenizer.from_pretrained(
      "tokenizerのパス", 
      use_fast=False
    )
    model = AutoModelForCausalLM.from_pretrained(
      "LLMのパス",
      load_in_8bit=True,
      torch_dtype=torch.float16,
      device_map="auto",
    )
  print("LLM読み込み終了。")
  return device,device1,tokenizer,model