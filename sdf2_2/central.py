from asd.voice.v2t import start_transcription
from asd.text_thinning.thinning import *
from asd.LLMot.loadingLLM import loadingLLM
from asd.memory.loading import loadtokenizer
from asd.LLMot.LLM import generate_one_token_at_a_time

from asd.memory.mem import sen2pr
from asd.memory.current_mem import cur
from asd.memory.current_mem import cur_w
from asd.voicevox.vv import t2v

if __name__ == "__main__":
  co=2
  sdf=0
  speaker="user"
  sistem="sistem"
  histry=[['',''],
          ['',''],
          ['',''],
          ['',''],
          ['',''],
          ['',''],
          ['',''],
          ['',''],
          ['',''],
          ['','']]
  #LLMの読み込み
  device,device1,tokenizer,model_LLM=loadingLLM()
  model_tokenizer=loadtokenizer()
  #会話機能起動
  while sdf==0:
    #t2v
    transcription = start_transcription(
      #model:'tiny.en', 'tiny', 'base.en', 'base', 'small.en', 'small', 'medium.en', 'medium', 'large-v1', 'large-v2', 'large'
      model="large-v2", device=device1, verbose=False, energy=400, dynamic_energy=True, pause=0.8, save_file=False, language='japanese'
    )
    sentence= next(transcription)
    sdf=thin0(sentence)
    print("文字起こし結果:", sentence)
    #文字起こし結果からLLMを起動すべきか判断
    sentence1,asd=thin1(sentence)
    if asd==0:
      #プロンプトを生成
      histry=cur(histry)
      prompt=sen2pr(sentence,speaker,sistem,histry,model_tokenizer)
      print(prompt)
      #LLM起動
      output=generate_one_token_at_a_time(prompt,tokenizer,model_LLM)
      resp=thin2(output)
      print(resp)
      cur_w(histry,prompt,resp)
      #返答音声変換
      t2v(resp,co)
      #savememo(sentence,resp)
    else:
      print("<NL>"+sistem+":\n",sentence1)
      #返答音声変換
      t2v(sentence1,co)