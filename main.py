from openai import OpenAI
import speech_recognition as sr
import os
import pyttsx3
from dotenv import load_dotenv
import tkinter as tk
import threading

load_dotenv('./.env')

class SpeechToSpeechBot:
    client = OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY"),
    )
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.setProperty('rate', 150)

    def generate_response(self, prompt):
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant.From now on, please refer to yourself as Jarvis."},
                {"role": "user", "content": prompt}
            ]
        )
        return response
    
    def text_to_speech(self, text):
            engine = pyttsx3.init()
            engine.say(text)
            engine.runAndWait()

    def speech_to_text(self):
        while True: 
            recognizer = sr.Recognizer()
            with sr.Microphone() as source:
                print("Listening...")
                sr.pause_threshold = 1
                audio = recognizer.listen(source)
                try:
                    print("Recognizing...")
                    text = recognizer.recognize_google(audio)
                    response = self.generate_response(text)
                    self.text_to_speech(response.model_dump()['choices'][0]['message']['content'])

                except Exception as e:
                    print(e)
                    self.text_to_speech("Sorry, I didn't get that. Please try again.")

t = threading.Thread(target=SpeechToSpeechBot().speech_to_text())
t.daemon = True
t.start()

