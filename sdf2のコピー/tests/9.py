import openai
import time
import requests
import pygame
import os
from janome.tokenizer import Tokenizer

# OpenAI APIキーの設定
openai.api_key = 'your-api-key'

tokenizer = Tokenizer()

VOICEVOX_API_URL = "http://localhost:50021"

def text_to_speech(text):
    params = {
        "text": text,
        "speaker": 1  # 話者IDを指定（例: 1）
    }
    response = requests.post(f"{VOICEVOX_API_URL}/audio_query", params=params)
    if response.status_code != 200:
        print("Audio query failed.")
        return
    audio_query = response.json()
    
    synthesis_response = requests.post(f"{VOICEVOX_API_URL}/synthesis", json=audio_query)
    if synthesis_response.status_code != 200:
        print("Synthesis failed.")
        return
    
    with open('current_word.wav', 'wb') as f:
        f.write(synthesis_response.content)
    
    pygame.mixer.init()
    pygame.mixer.music.load('current_word.wav')
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        time.sleep(0.1)
    os.remove('current_word.wav')

def is_word_complete(word):
    tokens = list(tokenizer.tokenize(word))
    return len(tokens) == 1 and tokens[0].surface == word

def generate_and_speak(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=100,
        stream=True
    )

    word = ""
    past_words = set()
    for chunk in response:
        if 'choices' in chunk and chunk['choices'][0]['text']:
            token = chunk['choices'][0]['text']
            if token.strip():
                word += token
                print(token, end='', flush=True)
                if is_word_complete(word.strip()):
                    if word.strip() not in past_words:
                        past_words.add(word.strip())
                        text_to_speech(word.strip())
                    word = ""

if __name__ == "__main__":
    user_prompt = "Your initial prompt here"
    generate_and_speak(user_prompt)