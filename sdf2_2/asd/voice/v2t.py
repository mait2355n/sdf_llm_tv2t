import io
from pydub import AudioSegment
import speech_recognition as sr
import whisper
import queue
import tempfile
import os
import threading
import torch
import numpy as np

def record_audio(audio_queue, energy, pause, dynamic_energy, save_file, temp_dir):
    # 音声認識器を読み込み、初期のエネルギー閾値とポーズの閾値を設定します
    r = sr.Recognizer()
    r.energy_threshold = energy
    r.pause_threshold = pause
    r.dynamic_energy_threshold = dynamic_energy
    with sr.Microphone(sample_rate=16000) as source:
        print("音声取得中。")
        i = 0
        while True:
            # 音声を取得してwavファイルに保存します
            audio = r.listen(source)
            if save_file:
                data = io.BytesIO(audio.get_wav_data())
                audio_clip = AudioSegment.from_file(data)
                filename = os.path.join(temp_dir, f"temp{i}.wav")
                audio_clip.export(filename, format="wav")
                audio_data = filename
            else:
                torch_audio = torch.from_numpy(np.frombuffer(audio.get_raw_data(), np.int16).flatten().astype(np.float32) / 32768.0)
                audio_data = torch_audio
            audio_queue.put_nowait(audio_data)
            i += 1

def transcribe_audio(audio_data, audio_model, language):
    if language == 'japanese':
        result = audio_model.transcribe(audio_data, language='japanese')
    else:
        result = audio_model.transcribe(audio_data)
    return result

def start_transcription(model, device,verbose, energy, dynamic_energy, pause, save_file,language):
    temp_dir = tempfile.mkdtemp() if save_file else None
    audio_model = whisper.load_model(model).to(device)
    audio_queue = queue.Queue()
    threading.Thread(target=record_audio,
                     args=(audio_queue, energy, pause, dynamic_energy, save_file, temp_dir)).start()
    while True:
        audio_data = audio_queue.get()
        result = transcribe_audio(audio_data, audio_model, language)

        if not verbose:
            predicted_text = result["text"]
            yield predicted_text
        else:
            yield result
        if save_file:
            os.remove(audio_data)
    
if __name__=="__main__":
    print("ok")