import speech_recognition as sr
import pathlib
from pydub import AudioSegment

class VoiceToText():

    def __init__(self):
        self.r = sr.Recognizer()

    def convert(self):
        try:
            tmp_file = str(pathlib.Path().resolve())+"/cache/tmp_voice.ogg"
            wfn = tmp_file.replace('.ogg','.wav')
            x = AudioSegment.from_ogg(tmp_file)
            x.export(wfn, format='wav')
            with sr.AudioFile(wfn) as source:
                audio_data = self.r.record(source)
        
            text = self.r.recognize_google(audio_data,language="es-ES")
            return text
        except Exception as e:
            print(str(e))
            return ""
