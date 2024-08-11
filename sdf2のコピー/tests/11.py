import requests
import pygame
import os
import time

VOICEVOX_API_URL = "http://localhost:50021"

def text_to_speech(text):
    # audio_queryのリクエストボディを作成
    audio_query_params = {
        "text": text,
        "speaker": 1  # 話者IDを指定（例: 1）
    }
    
    # audio_queryのリクエストを送信
    response = requests.post(f"{VOICEVOX_API_URL}/audio_query", json=audio_query_params)
    if response.status_code != 200:
        print(f"Audio query failed with status code: {response.status_code}")
        print(response.text)
        return
    audio_query = response.json()
    
    # synthesisのリクエストを送信
    synthesis_response = requests.post(f"{VOICEVOX_API_URL}/synthesis", json=audio_query)
    if synthesis_response.status_code != 200:
        print(f"Synthesis failed with status code: {synthesis_response.status_code}")
        print(synthesis_response.text)
        return
    
    # 音声データをファイルに保存
    with open('test_audio.wav', 'wb') as f:
        f.write(synthesis_response.content)
    
    # 音声を再生
    pygame.mixer.init()
    pygame.mixer.music.load('test_audio.wav')
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        time.sleep(0.1)
    os.remove('test_audio.wav')

if __name__ == "__main__":
    text = "こんにちは、これはテストです。"
    text_to_speech(text)