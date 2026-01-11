# pip install gtts pygame

import os
from gtts import gTTS
#import pygame
from time import sleep

text = "Привіт! Як твої справи? Сподіваюсь все добре ^_^"
language = "uk"
output_filename = "temp_audio_gtts.mp3"
tts = gTTS(
    text=text,
    lang=language,
    slow=False,
    tld='co.uk'
)
tts.save(output_filename)

pygame.mixer.init()

pygame.mixer.music.load(output_filename)
pygame.mixer.music.play()

print("Початок програвання...")
while pygame.mixer.music.get_busy():
    sleep(0.1)

print("закынчення програвання...")

if os.path.exists(output_filename):
    pygame.mixer.quit()
    os.remove(output_filename)