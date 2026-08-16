from piper import PiperVoice
import sounddevice as sd
import behavior.state_machine as machine 

voice = PiperVoice.load("piper_voice/en_US-ryan-medium.onnx")

def vocal(texte):
    for chunk in voice.synthesize(texte):
        # chunk.audio_float_array contient l'audio dcp jutilse sounddevice
        
        sd.play(chunk.audio_float_array, 22050) # baudrate from the json of the onnx file
        sd.wait()
        pass