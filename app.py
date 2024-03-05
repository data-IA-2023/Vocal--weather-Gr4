from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
import os
import azure.cognitiveservices.speech as speechsdk
from dotenv import load_dotenv
import requests

app = FastAPI()

templates = Jinja2Templates("templates")

load_dotenv()

def recognize_from_microphone():
    # This example requires environment variables named "SPEECH_KEY" and "SPEECH_REGION"
    speech_config = speechsdk.SpeechConfig(subscription=os.environ.get('SPEECH_KEY'), region=os.environ.get('SPEECH_REGION'))
    speech_config.speech_recognition_language=os.environ.get('SPEECH_LANG')

    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    print("Speak into your microphone.")
    speech_recognition_result = speech_recognizer.recognize_once_async().get()
    if speech_recognition_result.reason == speechsdk.ResultReason.RecognizedSpeech:
        recognized_text = speech_recognition_result.text
        print("Recognized: {}".format(recognized_text))
        return recognized_text

    elif speech_recognition_result.reason == speechsdk.ResultReason.NoMatch:
        print("No speech could be recognized: {}".format(speech_recognition_result.no_match_details))
        return speech_recognition_result.no_match_details
    
    elif speech_recognition_result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = speech_recognition_result.cancellation_details
        print("Speech Recognition canceled: {}".format(cancellation_details.reason))

        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))
            print("Did you set the speech resource key and region values?")
    
    return cancellation_details.error_details

def search(city,country,lang):
    url = f"https://foreca-weather.p.rapidapi.com/location/search/{city}"

    querystring = {"lang":lang,"country":country}

    headers = {
	"X-RapidAPI-Key": os.environ.get('X-RapidAPI-Key'),
	"X-RapidAPI-Host": os.environ.get('X-RapidAPI-Host')
    }

    searched = requests.get(url, headers=headers, params=querystring)
    print(searched)

    return searched.json()


@app.get("/")
def read_root(request: Request, city: str = "Tours", lang: str = "fr"):
    url = f"https://foreca-weather.p.rapidapi.com/location/search/{city}"

    querystring = {"lang":lang}

    headers = {
	"X-RapidAPI-Key": os.environ.get('X-RapidAPI-Key'),
	"X-RapidAPI-Host": os.environ.get('X-RapidAPI-Host')
    }

    searched = requests.get(url, headers=headers, params=querystring)

    search_result   = searched.json()

    return search_result['locations'][0]


    response = recognize_from_microphone()
    return templates.TemplateResponse("index.html",{"request": request,"response": response,"searched":searched})

