import speech_recognition as sr
import pathlib


class VoiceToText():

    def __init__(self):
        self.r = sr.Recognizer()

    def convert(self):
        try:
            with sr.AudioFile(str(pathlib.Path().resolve())+"/cache/tmp_voice.mp3") as source:
                # listen for the data (load audio to memory)
                audio_data = self.r.record(source)
                # recognize (convert from speech to text)
                text = self.r.recognize_google(audio_data)
                return text
        except:
            return ""
