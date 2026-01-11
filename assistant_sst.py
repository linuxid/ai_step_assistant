import sounddevice as sd
import numpy as np
import speech_recognition as sr
import io
import wave
from datetime import datetime

# ==================== Налаштування ====================
sample_rate = 44100 #Hz
duration = 5  # sec
silence_threshold = 0.01  # поріг RMS для визначення тиші
min_speech_rms = 0.02  # мінімальна енергія, щоб записати
log_file = "log_speech.txt"

recognizer = sr.Recognizer()
recognizer.energy_threshold = 300  # початковий поріг
recognizer.dynamic_energy_threshold = True  # адаптація порогу під шум

# ==================== Функції ====================
def is_silent(audio_chunk):
    rms = np.sqrt(np.mean(audio_chunk**2))
    return rms < silence_threshold

def log_text(text):
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {text}\n")

def listen_and_recognize():
    print("🎤 Слухаю... (скажи 'стоп' щоб завершити)")
    
    recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='float32')
    sd.wait()

    if is_silent(recording):
        return None

    audio_int16 = np.int16(recording * 32767)

    buf = io.BytesIO()
    with wave.open(buf, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)  # 16-bit
        wf.setframerate(sample_rate)
        wf.writeframes(audio_int16.tobytes())
    buf.seek(0)

    with sr.AudioFile(buf) as source:
        audio_data = recognizer.record(source)
    try:
        return recognizer.recognize_google(audio_data, language="uk-UA")
    except sr.UnknownValueError:
        return "Не розпізнав..."
    except sr.RequestError as e:
        return f"Помилка сервісу: {e}"

# ==================== Основний цикл ====================
while True:
    text = listen_and_recognize()
    if text is None:
        print("🕒 Тиша або шум — пропускаю фрагмент")
        continue

    print("Ти:", text)
    log_text(text)

    if "стоп" in text.lower():
        print("Асистент: Завершую роботу.")
        break
