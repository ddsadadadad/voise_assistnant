import random
import speech_recognition
import pygame
import threading
import random
import speech_recognition as sr
from gtts import gTTS
import os
from playsound import playsound
import pygame
import random
import json
import datetime
import webbrowser
import requests
import smtplib 
import pywhatkit
import pyautogui
import time
import pyttsx3
import threading
import pyowm
import subprocess

sr = speech_recognition.Recognizer()
sr.pause_threshold = 0.5

commands_dict = {
    'commands': {
        'play_music': ['включить музыку', 'дискотека'],
        'set_timer': ['установить таймер', 'таймер'],
        'open_youtube': ['открыть youtube', 'открой youtube','youtube', 'youtube.com','ютуб', 'ютуб.com'],
        'create_task': ['сделать задачу', 'сделай задачу', 'задача', ' сделай заметку', 'заметка','создай заметку'],
        'get_current_datetime': ['время','сколько времени','сейчас времени','текущее время','дата','дата и время'],
        'clear_cache_and_temp_files': ['очистить кеш','удалить кеш','очистить память','удалить память','очистка'],
        'chatgpt': ['chatgpt', 'chatgpt.com','открой chatgpt','чатгпт','открой чат'],
        'open_telegram_in_browser': ['telegram', 'telegram.com', 'открой telegram', 'открой телеграм', 'телеграм'],
        'open_github_in_browser': ['github', 'github.com', 'открой github', 'открой гитхаб', 'гитхаб'],
        'open_steam': ['открой Steam', 'запусти Steam', 'Steam', 'запустить Steam','хочу поиграть','стим'],
        'open_website': ['открыть сайт', 'открой сайт'],
        'google_search': ['поиск в Google', 'найти в Google', 'гугл', 'гугл поиск', 'гугл найти'],
    }
}

###################main commands###############

def speak(text):
    tts = gTTS(text=text, lang='ru')
    tts.save('output.mp3')
    pygame.mixer.init()
    pygame.mixer.music.load('output.mp3')
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    pygame.mixer.quit()

import time

def listen_command():
    is_listening = False  # Variable to track if the assistant is listening for commands
    timeout = 30  # The timeout duration in seconds
    silence_duration = 6  # Duration of silence to detect the end of a command

    while True:
        try:
            with speech_recognition.Microphone() as mic:
                sr.adjust_for_ambient_noise(source=mic, duration=0.5)
                audio = sr.listen(source=mic, timeout=timeout)

                if is_listening:
                    query = sr.recognize_google(audio_data=audio, language='ru-RU').lower()

                    if "помощник" in query:
                        speak("Слушаю. Пожалуйста, дайте команду.")
                    else:
                        return query

                if not is_listening:
                    is_listening = True
                    speak("Слушаю. Пожалуйста, дайте команду.")
                    continue

        except speech_recognition.WaitTimeoutError:
            # Timeout occurred, stop listening
            is_listening = False

        except speech_recognition.UnknownValueError:
            if is_listening:
                # Check for silence to detect the end of the command
                silence_start = time.time()
                while time.time() - silence_start < silence_duration:
                    audio = sr.listen(source=mic, timeout=silence_duration)
                    if audio.frame_data:
                        # Audio is detected, reset silence timer
                        silence_start = time.time()
                    else:
                        # Silence detected, break the loop
                        break
                return query  # Return the recognized command

        except Exception as e:
            print(f"An error occurred: {e}")

###################open brawser################

def open_github_in_browser():
    url = "https://github.com"
    webbrowser.open(url)
    speak("Открываю GitHub в браузере.")

def open_telegram_in_browser():
    url = "https://web.telegram.org/"
    webbrowser.open(url)
    speak("Открываю Telegram в браузере.")

def open_youtube():
    url = "https://www.youtube.com"
    webbrowser.open(url)
    speak("Открываю YouTube.")
def chatgpt():
    url = "https://chat.openai.com/chat"
    webbrowser.open(url)
    speak("Открываю ChatGPT.")

def open_website_command():
    speak("Какой сайт вы хотели бы открыть?")
    site_name = listen_command().lower()
    if "github" in site_name:
        open_website("https://github.com", "GitHub")
    elif "telegram" in site_name:
        open_website("https://web.telegram.org/", "Telegram")
    else:
        speak("Извините, не могу открыть этот сайт.")

def google_search_command():
    speak("Что вы хотели бы найти в Google?")
    query = listen_command().lower()
    google_search(query)

def open_website(url, site_name):
    webbrowser.open(url)
    speak(f"Открываю {site_name} в браузере.")

def google_search(query):
    search_url = f"https://www.google.com/search?q={query}"
    webbrowser.open(search_url)
    speak(f"Выполняю поиск в Google для запроса: {query}.")

################################################

####################date and time###############

def get_current_datetime():
    now = datetime.datetime.now()
    current_time = now.strftime("%Y-%m-%d %H:%M:%S")
    speak(f"Текущая дата и время: {current_time}")

def set_timer():
    speak("Пожалуйста, скажите через сколько минут включить таймер.")
    time_str = listen_command()
    try:
        minutes = int(time_str)
        if minutes > 0:
            speak(f"Таймер установлен на {minutes} минут.")
            time.sleep(minutes * 60)
            speak("Время таймера истекло.")
        else:
            speak("Пожалуйста, укажите положительное количество минут.")
    except ValueError:
        speak("Извините, не удалось распознать количество минут.")

################################################

###################windows and open commands####

def open_steam():
    try:
        steam_executable_path = "Путь к исполняемому файлу Steam.exe"
        subprocess.Popen([steam_executable_path])
        print("Steam успешно запущен.")
    except FileNotFoundError:
        print("Исполняемый файл Steam не найден. Пожалуйста, укажите правильный путь.")

################################################

####################other ommands###############

def help_command():
    available_commands = ", ".join([v[0] for v in commands_dict['commands'].values()])
    speak(f"Доступные команды: {available_commands}.")

def create_task():
    """Create a todo task"""
    
    print('Что добавим в список дел?')
    
    query = listen_command()
        
    with open('todo-list.txt', 'a', encoding='utf-8') as file:
        file.write(f'❗️ {query}\n')
        
    return f'Задача {query} добавлена в todo-list!'

################################################

####################start function##############

def main():
    while True:
        query = listen_command()

        for k, v in commands_dict['commands'].items():
            if query in v:
                print(globals()[k]())
                break

################################################

if __name__ == '__main__':
    main()