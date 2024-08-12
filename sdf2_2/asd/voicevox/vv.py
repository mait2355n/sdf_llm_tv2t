import requests
import json
from pydub import AudioSegment
from pydub.playback import play
import time
import tempfile
import os

def t2v(resp,co):
    res1 = requests.post('http://127.0.0.1:50021/audio_query', params={'text': resp, 'speaker': 30})
    res2 = requests.post('http://127.0.0.1:50021/synthesis', params={'speaker': 30}, data=json.dumps(res1.json()))
    data = res2.content
    
    if co==1:
        path = "data/file0"+str(co)+".wav"  # ファイルを保存したいパスを指定
        #print(path)
        with open(path, "wb") as file:
            file.write(data)
    else:
        # ファイルを保存したいパスを指定
        path = "data/file1"+str(co)+".wav"  
        with open(path, "wb") as file:
            #保存
            file.write(data)
            
        # pydubを使用して再生する
        audio = AudioSegment.from_wav(path)

        # 5秒地点からの部分を抽出
        start_time = 150
        segment = audio[start_time:]

        # 再生
        play(segment)
    return path