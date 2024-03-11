import os
import azure.cognitiveservices.speech as speechsdk
from dotenv import load_dotenv 
from transformers import AutoTokenizer, AutoModelForTokenClassification
from transformers import pipeline
import requests
from datetime import datetime
from dateutil import parser
import pytz
import re
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
    elif speech_recognition_result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = speech_recognition_result.cancellation_details
        print("Speech Recognition canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))
            print("Did you set the speech resource key and region values?")



response = recognize_from_microphone()
tokenizer = AutoTokenizer.from_pretrained("Jean-Baptiste/camembert-ner-with-dates")
model = AutoModelForTokenClassification.from_pretrained("Jean-Baptiste/camembert-ner-with-dates")

headers = {
	"X-RapidAPI-Key": os.environ.get('X-RapidAPI-Key'),
	"X-RapidAPI-Host": os.environ.get('X-RapidAPI-Host')
    }



############## search city ##################################
def search(city):
    urlsearch = f"https://foreca-weather.p.rapidapi.com/location/search/{city}"

    querysearch = {"lang":"fr"}

    headers = {
	"X-RapidAPI-Key": os.environ.get('X-RapidAPI-Key'),
	"X-RapidAPI-Host": os.environ.get('X-RapidAPI-Host')
    }

    searched = requests.get(urlsearch, headers=headers, params=querysearch)
    search_result   = searched.json()
    idcity = search_result['locations'][0]['id']
    return idcity



################## current weather #########################
def currentweather(id):
    querystring = {"tempunit":"C","lang":"fr"}
    urlcurrent = f"https://foreca-weather.p.rapidapi.com/current/{id}"
    current = requests.get(urlcurrent, headers=headers, params=querystring)
    current_result = current.json()


 # Chaîne de temps fournie
    temps_str = current_result['current']['time']

# Analyser la chaîne de temps en objet datetime avec prise en charge du fuseau horaire
    temps_obj = parser.isoparse(temps_str)

# Définir le fuseau horaire
    fuseau_horaire = pytz.timezone('Europe/Paris')  # Fuseau horaire de la France

# Appliquer le fuseau horaire à l'objet datetime
    temps_obj = temps_obj.astimezone(fuseau_horaire)

# Formatage de la date et de l'heure en français
    format_francais = "%d/%m/%Y %H:%M:%S"
    temps_formate = temps_obj.strftime(format_francais)

    print(current_result['current']['time'])
    print("Date et heure en français:", temps_formate)
    print(str(current_result['current']['temperature'])+'°C')



############## hourly weather ############################
def hourlyWeather(id,hours):
    querystring = {"tempunit":"C","lang":"fr","periods":str(hours)}
    urlcurrent = f"https://foreca-weather.p.rapidapi.com/forecast/hourly/{id}"
    current = requests.get(urlcurrent, headers=headers, params=querystring)
    current_result = current.json()
    #return print(current_result)


 # Chaîne de temps fournie
    temps_str = current_result['forecast'][hours-1]['time']

# Analyser la chaîne de temps en objet datetime avec prise en charge du fuseau horaire
    temps_obj = parser.isoparse(temps_str)

# Définir le fuseau horaire
    fuseau_horaire = pytz.timezone('Europe/Paris')  # Fuseau horaire de la France

# Appliquer le fuseau horaire à l'objet datetime
    temps_obj = temps_obj.astimezone(fuseau_horaire)

# Formatage de la date et de l'heure en français
    format_francais = "%d/%m/%Y %H:%M:%S"
    temps_formate = temps_obj.strftime(format_francais)

    print(current_result['forecast'][hours-1]['time'])
    print("Date et heure en français:", temps_formate)
    print(str(current_result['forecast'][hours-1]['temperature'])+'°C')





############## daily weather ############################
def dailyWeather(id,days):
    querystring = {"tempunit":"C","lang":"fr","periods":str(days)}
    urlcurrent = f"https://foreca-weather.p.rapidapi.com/forecast/daily/{id}"
    current = requests.get(urlcurrent, headers=headers, params=querystring)
    current_result = current.json()
    #return print(current_result)


 # Chaîne de temps fournie
    temps_str = current_result['forecast'][days-1]['date']

# Analyser la chaîne de temps en objet datetime avec prise en charge du fuseau horaire
    temps_obj = parser.isoparse(temps_str)

# Définir le fuseau horaire
    fuseau_horaire = pytz.timezone('Europe/Paris')  # Fuseau horaire de la France

# Appliquer le fuseau horaire à l'objet datetime
    temps_obj = temps_obj.astimezone(fuseau_horaire)

# Formatage de la date et de l'heure en français
    format_francais = "%d/%m/%Y %H:%M:%S"
    temps_formate = temps_obj.strftime(format_francais)

    print(current_result['forecast'][days-1]['date'])
    print("Date et heure en français:", temps_formate)
    print('température maximum :',str(current_result['forecast'][days-1]['maxTemp'])+'°C')
    print('température minimum :',str(current_result['forecast'][days-1]['minTemp'])+'°C')



##### Process text sample (from wikipedia)
nlp = pipeline('ner', model=model, tokenizer=tokenizer, aggregation_strategy="simple")
test = nlp(response)
IsMeteo = 'météo' in response.lower()
print(test)
idcity = ''  # Initialiser idcity en dehors de la boucle
if IsMeteo:
    for i in range(len(test)):
        if test[i]['entity_group'] == 'LOC':
            loc = test[i]['word']
        
    idcity = search(loc)
    for i in range(len(test)):
        if test[i]['entity_group'] == 'DATE':
            if test[i]['word'].lower() == 'demain':
                    date = 2
                    dailyWeather(idcity,date)

            elif 'après' in test[i]['word'].lower() and 'demain' in test[i]['word'].lower():
                    date = 3
                    dailyWeather(idcity,date)


            elif 'jour' in test[i]['word'].lower() or 'jours' in test[i]['word'].lower():
                    resultats = re.findall(r'\b\d+\b', test[i]['word'])
                    date = int(resultats[0])
                    dailyWeather(idcity,date)

            else:
                    resultats = re.findall(r'\b\d+\b', test[i]['word'])
                    date = int(resultats[0])
                    hourlyWeather(idcity,date)
        else:
            currentweather(idcity)
else:
    print("vous n'avez pas demander la météo")

