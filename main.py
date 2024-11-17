from vosk import Model, KaldiRecognizer
import pyaudio
import webbrowser
import pyttsx3 as voice

model = Model(r"C:\\Users\kingjr7\myProjects\jarvis\vosk-model-fr-0.22")
recognizer = KaldiRecognizer(model, 16000)
mic = pyaudio.PyAudio()
stream = mic.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)
stream.start_stream()

print("jarvis demarer")
voice.speak("jarvis demarer")
while True:
    data = stream.read(2048, exception_on_overflow=False)

    if recognizer.AcceptWaveform(data):
        text = recognizer.Result()
        command = text[14:-3]
        print(command)
        if("cherche sur youtube" in command):
            print("ok je lance ca")
            query = command.split("youtube", 1)[1].strip()
            print("query: ", query)
            webbrowser.open("www.youtube.com/results?search_query="+query)
        elif("cherche sur google" in command):
            print("ok j'effectue la recherche")
            query = command.split("google", 1)[1].strip()
            print("query: ", query)
            webbrowser.open("www.google.com/search?q="+query)
        elif(command in ["arrête toi", "arrête-toi", "arrête doigts"]):
            print("ok je m'arrette ")
            break
        elif(command == " " or command == ""):
            pass
        else:
            print("j'ai pas compris votre requette")
            voice.speak("j'ai pas compris votre requette")