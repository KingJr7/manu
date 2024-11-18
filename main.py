from vosk import Model, KaldiRecognizer
import pyaudio
import webbrowser
import pyttsx3 as voice
import time
import requests
import pyautogui

class Manu():
    def __init__(self):
        self.model = Model(r"C:\\Users\kingjr7\myProjects\jarvis\vosk-model-small-fr-0.22")
        self.recognizer = KaldiRecognizer(self.model, 16000)
        self.mic = pyaudio.PyAudio()
        self.stream = self.mic.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)
        
    def speak(self, prompt):
        voice.speak(prompt)

    def search_youtube(self, command):
        print("ok je lance ca")
        query = command.split("youtube", 1)[1].strip()
        print("query: ", query)
        webbrowser.open("www.youtube.com/results?search_query="+query)

    def search_google(self, command):
        print("ok j'effectue la recherche")
        query = command.split("google", 1)[1].strip()
        print("query: ", query)
        webbrowser.open("www.google.com/search?q="+query)

    def get_time(self):
        t = time.localtime()
        current_time = time.strftime("%H:%M:%S", t)
        self.speak(current_time)

    def get_weather(self):
        api_key = "40be06e91eb19dd2f39deeaa95807ba2"
        try:
            response = requests.get(f"http://api.openweathermap.org/geo/1.0/direct?q=Pointe-Noire,CG&limit=5&appid={api_key}")
            if response.status_code == 200:
                posts = response.json()
                lat = posts[0]['lat']
                lon = posts[0]['lon']
                print('lat: ',lat)
                print('lon: ', lon)
                try:
                    data = requests.get(f"https://api.openweathermap.org/data/3.0/onecall?lat=-4.7975373&lon=11.8503297&appid={api_key}")
                    print(f"https://api.openweathermap.org/data/3.0/onecall?lat=-4.7975373&lon=11.8503297&appid={api_key}")
                    if data.status_code == 200:
                        print(data.json())
                    else:
                        print('Error lors de la fetch de la weather:', data.status_code)
                        return None
                except requests.exceptions.RequestException as e:
                    print('Error: ', e)
                    return None

            else:
                print('Error:', response.status_code)
                return None
        except requests.exceptions.RequestException as e:
            print('Error: ', e)
            return None

    def volume_down(self):
        pyautogui.press("volumedown", 3)

    def volume_up(self):
        pyautogui.press("volumeup", 3)

    def volume_mute(self):
        pyautogui.press("volumemute")

    def demarrer(self):
        self.stream.start_stream()
        print("jarvis demarer")
        self.speak("jarvis demarer")
        while True:
            data = self.stream.read(2048, exception_on_overflow=False)

            if self.recognizer.AcceptWaveform(data):
                text = self.recognizer.Result()
                command = text[14:-3]
                print(command)
                if("cherche sur youtube" in command):
                    self.search_youtube(command)
                elif("cherche sur google" in command):
                    self.search_google(command)
                elif(command in ["arrête toi", "arrête-toi", "arrête doigts"]):
                    print("ok je m'arrette ")
                    self.speak("ok je m'arrette")
                    break
                elif(command in ["il est quelle heure"]):
                    self.get_time()
                elif("monte le volume" in command):
                    self.volume_up()
                elif("baisse le volume" in command):
                    self.volume_down()
                elif("coupe le volume" in command):
                    self.volume_mute()
                elif(command == " " or command == ""):
                    pass
                else:
                    print("j'ai pas compris votre requette")
                    self.speak("j'ai pas compris votre requette")

manu = Manu()
manu.demarrer()