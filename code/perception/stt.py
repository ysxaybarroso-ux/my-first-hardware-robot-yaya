from vosk import Model, KaldiRecognizer
import sounddevice as sd
import json

texte = ""

def Ecoute ():
    model_vosk = Model("vosk-model-small-en-us-0.15")
    recognizer = KaldiRecognizer(model_vosk , 16000)
    def Callback (indata , frames ,time , status):
        global texte
        if recognizer.AcceptWaveform(bytes(indata)):
            resultat = json.loads(recognizer.Result())
            texte = resultat["text"]
        
    with sd.InputStream(samplerate=16000, channels=1, callback=Callback):
        while True:
            pass
