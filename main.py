import sys
from dotenv import dotenv_values,load_dotenv
sys.path.append('modules')
from stt import *
import sounddevice as sd
import wave
import pyaudio
from scipy.io.wavfile import write
import spacy
import fr_core_news_sm
from regex import *
 

load_dotenv()

key=os.getenv("KEY1")
region=os.getenv("REGION")
endpoint=os.getenv("ENDPOINT")
language="fr-FR"

filename="temp/test.wav"
"""
# Sampling frequency
freq = 44100
 
# Recording duration
duration = 5
 
# Start recorder with the given values 
# of duration and sample frequency
recording = sd.rec(int(duration * freq), 
                   samplerate=freq, channels=2)
 
# Record audio for the given number of seconds
sd.wait()
 
# This will convert the NumPy array to an audio
# file with the given sampling frequency
write("temp/recording.wav", freq, recording)"""
# result=stt(key,filename,language,region)
result="Quelle sera le temps à Tours dans 17 heures et 30 minutes ?"




features=analyse_text(result)


print(features)
"""
nlp = spacy.load('fr_core_news_md')

doc = nlp(result)

print(doc.ents)

match = re.search(pattern, 'foo@example.com')

for ent in doc.ents:
    print(ent.text, ent.start_char, ent.end_char, ent.label_)"""