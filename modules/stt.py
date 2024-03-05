import os
import azure.cognitiveservices.speech as speechsdk
from dotenv import dotenv_values,load_dotenv

def stt(speech_key,speech_key,filename):
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=speech_key)

    #audio_config = speechsdk.audio.AudioConfig(filename=filename)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)
    result = speech_recognizer.recognize_once_async().get()
    return result.text