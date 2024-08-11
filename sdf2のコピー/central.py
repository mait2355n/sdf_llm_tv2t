
from asd.LLMot.loadingLLM import loadingLLM
from asd.memory.loading import loadtokenizer
from asd.LLMot.tests.LLM import generate_one_token_at_a_time
from asd.memory.mem import sen2pr
from asd.memory.vec_momory import *
from asd.memory.tests.sumple import sumple
from asd.prompt.pr_construction 

if __name__ == "__main__":
  co=2
  sdf=0
  speaker="mait"
  sistem="sistem"
  sentence,memory,related,histry=sumple()
  #LLMの読み込み
  device,device1,tokenizer,model_LLM=loadingLLM()
  model_tokenizer=loadtokenizer()
  #データベースのセッティング
  if not os.path.exists(f"data/vec_mem"):
    os.makedirs(f"data/vec_mem")
    print(f"フォルダ 'data/vec_mem' を作成しました。")
    resped=save_search("例文1a",1,model_tokenizer,"prompt",k=1)
    save_search("例文1b",2,model_tokenizer,"resp",k=1)
    resped=save_search("例文2a",1,model_tokenizer,"prompt",k=1)
    save_search("例文2b",2,model_tokenizer,"resp",k=1)
    resped=save_search("例文3a",1,model_tokenizer,"prompt",k=1)
    save_search("例文3b",2,model_tokenizer,"resp",k=1)
  #会話機能起動
  while sdf==0:
    sentence=input("入力:")
    if sentence=="quit":
      asd=1
      sdf=1
    if asd==0:
      num=1
      #記憶を呼び出し,プロンプトをベクトル化して保存
      resped=save_search(sentence,num,model_tokenizer,"prompt",k=3)
      #プロンプトを生成
      prompt=sen2pr(sentence,memory,speaker,sistem,resped)
      print(prompt)
      #LLM起動
      output=generate_one_token_at_a_time(prompt,tokenizer,model_LLM)
      num=2
      print(output)
      save_search(output,2,model_tokenizer,"resp",k=0)
      
      #savememo(sentence,resp)
    else:
      print("<NL>"+sistem+":\n",sentence)
      