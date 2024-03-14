from connect2db import *
import azure.cognitiveservices.speech as speechsdk
from transformers import AutoTokenizer, AutoModelForTokenClassification
from transformers import pipeline
import requests
from datetime import datetime, date
from dateutil import parser
import pytz
import re
#import sounddevice as sd
#import wave
#import pyaudio
#from scipy.io.wavfile import write

headers = {
	"X-RapidAPI-Key": os.environ.get('X-RapidAPI-Key'),
	"X-RapidAPI-Host": os.environ.get('X-RapidAPI-Host')
    }



def recognize_from_microphone(audio):
    speech_config = speechsdk.SpeechConfig(subscription=os.environ.get('SPEECH_KEY'), region=os.environ.get('SPEECH_REGION'))
    speech_config.speech_recognition_language=os.environ.get('SPEECH_LANG')

    audio_config = speechsdk.audio.AudioConfig(filename=audio)
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
    """This function takes a city ID as input and uses the weather API to retrieve the current weather data for that city. It parses the response to extract relevant information like temperature, chance of rain, wind speed, cloud cover, and formats the date and time in French according to the Paris time zone."""
    querystring = {"tempunit":"C","lang":"fr","tz":"Europe/Paris","dataset": 'full'}
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


    result = "Date et heure en français : " + temps_formate +'\nTempérature : ' + str(current_result['current']['temperature'])+'°C'+'\nProbabilité de pluie : ' + str(current_result['current']['precipProb'])+' %' +'\nVitesse du vent : ' + str(current_result['current']['windSpeed'])+' m/s'+'\nPrésence nuageuse : ' + str(current_result['current']['cloudiness'])+' %'  
    return result, current




############## hourly weather ############################
def hourlyWeather(id,hours):
    """This function takes a city ID and the number of hours as input and uses the weather API to retrieve the hourly weather forecast for that city for the specified number of hours. It parses the response to extract relevant information and formats the date and time in French according to the Paris time zone."""
    querystring = {"tempunit":"C","lang":"fr","tz":"Europe/Paris","periods":str(hours),"dataset": 'full'}
    urlcurrent = f"https://foreca-weather.p.rapidapi.com/forecast/hourly/{id}"
    current = requests.get(urlcurrent, headers=headers, params=querystring)
    current_result = current.json()
    #return print(len(current_result))


    # Chaîne de temps fournie
    temps_str = current_result['forecast'][-1]['time']

    # Analyser la chaîne de temps en objet datetime avec prise en charge du fuseau horaire
    temps_obj = parser.isoparse(temps_str)

    # Définir le fuseau horaire
    fuseau_horaire = pytz.timezone('Europe/Paris')  # Fuseau horaire de la France

    # Appliquer le fuseau horaire à l'objet datetime
    temps_obj = temps_obj.astimezone(fuseau_horaire)

    # Formatage de la date et de l'heure en français
    format_francais = "%d/%m/%Y %H:%M:%S"
    temps_formate = temps_obj.strftime(format_francais)

    print("Date et heure en français:", temps_formate)
    print(str(current_result['forecast'][-1]['temperature'])+'°C')

    result = "Date et heure en français : " + temps_formate +'\nTempérature : ' + str(current_result['forecast'][-1]['temperature'])+'°C'+'\nProbabilité de pluie : ' + str(current_result['forecast'][-1]['precipProb'])+' %' +'\nVitesse du vent : ' + str(current_result['forecast'][-1]['windSpeed'])+' m/s'+'\nPrésence nuageuse : ' + str(current_result['forecast'][-1]['cloudiness'])+' %'
    return result, current

################# dat day weather ########################
def datDayWeather(id,date):
    """This function takes a city ID and a date as input and uses the weather API to retrieve the weather data for that specific date. It parses the response to extract relevant information and formats the date and time in French according to the Paris time zone."""
    match = False
    querystring = {"tempunit":"C","lang":"fr","tz":"Europe/Paris","periods":"15","dataset": 'full'}
    urlcurrent = f"https://foreca-weather.p.rapidapi.com/forecast/daily/{id}"
    current = requests.get(urlcurrent, headers=headers, params=querystring)
    current_result = current.json()
    #return print(current_result)
    for i in range(len(current_result['forecast'])):
            if current_result['forecast'][i]['date'] == str(date):
                    datday = current_result['forecast'][i]
                    match = True
    if match == True : 
                # Chaîne de temps fournie
                    temps_str = datday['date']

                # Analyser la chaîne de temps en objet datetime avec prise en charge du fuseau horaire
                    temps_obj = parser.isoparse(temps_str)

                # Définir le fuseau horaire
                    fuseau_horaire = pytz.timezone('Europe/Paris')  # Fuseau horaire de la France

                # Appliquer le fuseau horaire à l'objet datetime
                    temps_obj = temps_obj.astimezone(fuseau_horaire)

                # Formatage de la date et de l'heure en français
                    format_francais = "%d/%m/%Y"
                    temps_formate = temps_obj.strftime(format_francais)

                    result = "Date et heure en français : " + temps_formate +'\nTempérature maximum : ' + str(datday['maxTemp'])+'°C\n' + 'Température minimum : ' + str(datday['minTemp'])+'°C' +'\nProbabilité de pluie : ' + str(datday['precipProb'])+' %' +'\nVitesse du vent : ' + str(datday['maxWindSpeed'])+' m/s'+'\nPrésence nuageuse : ' + str(datday['cloudiness'])+' %'
                    return result, current
    else : 
                    raise Exception ("je n'ai pas compris votre demande veuillez réessayer")





    ############## daily weather ############################
def dailyWeather(id,days):
    """This function takes a city ID and the number of days as input and uses the weather API to retrieve the daily weather forecast for that city for the specified number of days. It parses the response to extract relevant information and formats the date and time in French according to the Paris time zone."""
    querystring = {"tempunit":"C","lang":"fr","tz":"Europe/Paris","periods":str(days),"dataset": 'full'}
    urlcurrent = f"https://foreca-weather.p.rapidapi.com/forecast/daily/{id}"
    current = requests.get(urlcurrent, headers=headers, params=querystring)
    current_result = current.json()
    #return print(current_result)

 # Chaîne de temps fournie
    temps_str = current_result['forecast'][-1]['date']

# Analyser la chaîne de temps en objet datetime avec prise en charge du fuseau horaire
    temps_obj = parser.isoparse(temps_str)

# Définir le fuseau horaire
    fuseau_horaire = pytz.timezone('Europe/Paris')  # Fuseau horaire de la France

# Appliquer le fuseau horaire à l'objet datetime
    temps_obj = temps_obj.astimezone(fuseau_horaire)

# Formatage de la date et de l'heure en français
    format_francais = "%d/%m/%Y"
    temps_formate = temps_obj.strftime(format_francais)

    result = "Date et heure en français : " + temps_formate +'\nTempérature maximum : ' + str(current_result['forecast'][-1]['maxTemp'])+'°C\n' + 'Température minimum : ' + str(current_result['forecast'][-1]['minTemp'])+'°C' +'\nProbabilité de pluie : ' + str(current_result['forecast'][-1]['precipProb'])+' %' +'\nVitesse du vent : ' + str(current_result['forecast'][-1]['maxWindSpeed'])+' m/s'+'\nPrésence nuageuse : ' + str(current_result['forecast'][-1]['cloudiness'])+' %'
    return result, current 
    ######################### weatherMatch ########################

def weatherMatch(id,data):
    """This function takes a city ID and user text as input. It uses regular expressions to match weather-related keywords and phrases in the text and calls the appropriate weather function (currentweather, hourlyWeather, datDayWeather, or dailyWeather) based on the matched pattern. It also handles cases where the user specifies dates using expressions like "today," "tomorrow," or specific days of the week."""
    global mois_fr
    if re.search(r'demain', data.lower()):
                    dateWeather = 2
                    weather = dailyWeather(id,dateWeather)
                    return weather

    elif re.search(r'après(-| )demain', data.lower()):
                    dateWeather = 3
                    weather = dailyWeather(id,dateWeather)
                    return weather


    elif 'jour' in data.lower() or 'jours' in data.lower():
                    resultats = re.findall(r'\b\d+\b', data)
                    dateWeather = int(resultats[0]) + 1
                    if dateWeather > 15 :
                            raise Exception("je n'ai pas compris votre demande veuillez réessayer")
                    else : 
                        weather = dailyWeather(id,dateWeather)
                        return weather

    elif 'h' in data.lower() or 'heure' in data.lower() or 'heures' in data.lower():
                    resultats   = re.findall(r'\b\d+\b', data)
                    dateWeather = int(resultats[0]) + 1
                    if dateWeather > 169:
                        raise Exception("je n'ai pas compris votre demande veuillez réessayer")
                    else : 
                        weather = hourlyWeather(id,dateWeather)
                        return weather

    elif re.search(r'janvier|février|mars|avril|mai|juin|juillet|août|septembre|octobre|novembre|décembre', data):
                    jour = re.findall(r'\b\d+\b', data)
                    mois = re.findall(r'janvier|février|mars|avril|mai|juin|juillet|août|septembre|octobre|novembre|décembre', data)
                    actualYear = datetime.today().year
                    dateWeather =f'{jour[0]} {mois[0]} {actualYear}'
                    # Extraire le jour, le mois et l'année
                    jour, mois_str, annee = dateWeather.split()

                    # Convertir le mois en chiffre en utilisant le dictionnaire de correspondance
                    mois = mois_fr.get(mois_str.lower())

                    # Créer un objet datetime
                    date_obj = date(int(annee), mois, int(jour))
                    weather  = datDayWeather(id,date_obj)
                    return weather

    elif data =="aujourd'hui" or data =='':
                    weather = currentweather(id)
                    return weather


mois_fr = {
        'janvier': 1, 'février': 2, 'mars': 3, 'avril': 4,
        'mai': 5, 'juin': 6, 'juillet': 7, 'août': 8,
        'septembre': 9, 'octobre': 10, 'novembre': 11, 'décembre': 12
    } 


##### Process text sample (from wikipedia)
def execute_cmd(audio):
    """This is the endpoint function, it takes an audio filepath performs stt then ner and calls the foreca api to return the desired weather information."""
    global mois_fr      
    response = recognize_from_microphone(audio)
    tokenizer = AutoTokenizer.from_pretrained("Jean-Baptiste/camembert-ner-with-dates")
    model = AutoModelForTokenClassification.from_pretrained("Jean-Baptiste/camembert-ner-with-dates")    

    nlp = pipeline('ner', model=model, tokenizer=tokenizer, aggregation_strategy="simple")
    camembert = nlp(response)
    IsMeteo   = 'météo' in response.lower() or 'temps' in response.lower() or 'beau' in response.lower() or 'mauvais' in response.lower()
    print(camembert)
    idcity       = ''  # Initialiser idcity en dehors de la boucle
    locword      = ''
    dateword     = ''
    feedback     = ''
    datescore    = ''
    if IsMeteo:
        for i in range(len(camembert)):
            if camembert[i]['entity_group'] == 'LOC':
                locword  = camembert[i]['word']
                locscore = camembert[i]['score']
            if camembert[i]['entity_group'] == 'DATE':
                dateword = camembert[i]['word']
                datescore = camembert[i]['score']

        if locword:      
            idcity           = search(locword)
            weather          = weatherMatch(idcity,dateword)
            weather_result   = "Lieu : " + locword + "\n" + weather[0]
            weather_request  = weather[1]
            weatherFinal=(response,weather_request,weather_result,locword,locscore,dateword,datescore,feedback)
            return weatherFinal
        else : 
            raise Exception("je n'ai pas compris votre demande veuillez réessayer")
    else:
        return None