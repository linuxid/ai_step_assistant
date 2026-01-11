# pip install sounddevice    (pyaudio)
# pip install SpeechRecognition
# pip install numpy

import sounddevice as sd
import numpy as np
import wave
import io
import speech_recognition as sr

# *wav

buf = io.BytesIO()
r = sr.Recognizer()

print("Говори...")

duration = 5
rate = 44100

record = sd.rec(int(duration * rate), samplerate=rate, channels=1, dtype='float32')
sd.wait()

record_int16 = np.int16(record * 32767)

with wave.open(buf, 'wb') as wb:
    wb.setnchannels(1)
    wb.setsampwidth(2)
    wb.setframerate(rate)
    wb.writeframes(record_int16.tobytes())

buf.seek(0)

with sr.AudioFile(buf) as audio:
    audio_data = r.record(audio)

text = r.recognize_google(audio_data, language="uk-UA")

print(text)