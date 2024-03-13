import re
import pickle
import os
import copy
import ast
from builtins import eval
from datapackage import Package
import datetime

if not os.path.isfile("cities.pkl"):
    package = Package('https://datahub.io/core/world-cities/datapackage.json')

    for resource in package.resources:
        if resource.descriptor['datahub']['type'] == 'derived/csv':
            cities=[e[0].lower() for e in resource.read()]
            with open('cities.pkl', 'wb') as f:
                pickle.dump(cities, f)
else :
    with open('cities.pkl', 'rb') as pickle_file:
        cities=pickle.load(pickle_file)

date_pattern = r"([0-9]|[0-2][0-9]|3[0-1])( (janvier|février|mars|avril|mai|juin|juillet|août|septembre|octobre|novembre|décembre) 202[0-9]|(/| |-|.)(1[0-2]|[1-9])(/| |-|.)20[0-9][0-9])"

day_pattern = r"lundi|mardi|mercredi|jeudi|vendredi|samedi|dimanche"

cities_pattern = re.compile('^'+'|^'.join(cities)+'|'+'| '.join(cities))

info_pattern= r"météo|température|pluie|((beau|mauvais)( |-))?temps"

relative_date_pattern= r"demain|aujourd('| )hui|après(-| )demain|hier|avant( |-)hier|(dans |(il )?y ?a )?([0-9]|une?|deux|trois|quatres?|cinq|six|sept|huit|neuf|dix) (jours?|semaines?|mois)( dans le (futur|passé))?"

time_pattern=r"(dans |(il )?y ?a |(à |a ))?((([0-1][0-9]|2[0-3])(:| ?h| ?H)[0-5][0-9])|([0-1][0-9]|2[0-3]) ?(heures?( et)?|(et)?)?( ?(([0-5][0-9]|[0-9])( minutes?)?|(( |-)(demi|quart))|(moins( |-)quart)))?)"

def match_pattern(pattern,text):
    match=re.search(pattern, text)
    if match:
        return match.group()
    return ""

def extract_features(text):
    global date_pattern,cities_pattern,info_pattern,relative_day_pattern,time_pattern,day_pattern
    patterns={"date":date_pattern,"city":cities_pattern,"info":info_pattern,"relative_date":relative_date_pattern,"time":time_pattern,"day":day_pattern}
    features={}
    for pattern in patterns.keys():
        match=match_pattern(patterns[pattern],text.lower())
        if match != "":
            features[pattern]=match
            if match[-1] in [" ","?",",",".",":",";"] : features[pattern]=match[:-1]
            if match[0] in [" ","?",",",".",":",";"] : features[pattern]=match[1:]
    return features

def analyse_text(text):
    R=[]
    text2=copy.deepcopy(text.lower())
    while extract_features(text2) != {}:
        text3=copy.deepcopy(text2)
        R.append(extract_features(text2))
        for e in extract_features(text2).values():
            text3=text3.replace(e,"",1)
        text2=text3
    return R

def useful_information(text):
    L=analyse_text(text)
    L1=copy.deepcopy(L)
    for i in range(len(L)):
        if "relative_date" in L[i].keys() and "time" in L[i].keys():
            if "day" in L[i].keys() : del L1[i]["day"]
            for e in [("une","1"),("deux","2"),("trois","3"),("quatre","4"),("quatres","4"),("cinq","5"),("six","6"),("sept","7"),("huit","8"),("neuf","9"),("dix","10")]:
                L1[i]["relative_date"]=L1[i]["relative_date"].replace(e[0],e[1])
            for e in [("demain","+1"),("après","+2"),("hier","-1"),("avant","-2"),("dans le futur",""),("dans le passé","*(-1)")]:
                L1[i]["relative_date"]=L1[i]["relative_date"].replace(e[0],e[1])
            if L[i]["relative_date"][:2]=="il":
                L1[i]["relative_date"]=L1[i]["relative_date"]+" passé"
            L1[i]["relative_date"]=L1[i]["relative_date"].replace(" ","").replace("dans","").replace("ilya","-").replace("ya","-")
            if re.search(r"semaines?", L[i]["relative_date"]):
                L1[i]["relative_date"]=L1[i]["relative_date"].replace("semaine","*7").replace("semaines","*7").replace("s","")
            L1[i]["relative_date"]=L1[i]["relative_date"].replace("mois","*30")
            L1[i]["relative_date"]=L1[i]["relative_date"].replace("jour","*1")
            s=L1[i]["relative_date"]
            L1[i]["relative_date"]=eval(s)
            current_date = datetime.datetime.now()
            date=current_date+datetime.timedelta(days=L1[i]["relative_date"])
            L1[i]["true_date"]=date.date().strftime('%m/%d/%Y')
        if "info" in L[i].keys():
            if L[i]["info"]=="temps":L1[i]["info"]="météo"
        if "day" in L[i].keys():
            current_date = datetime.datetime.now()
            weekday_number = current_date.strftime('%w')
            for e in [("lundi",0),("mardi",1),("mercredi",2),("jeudi",3),("vendredi",4),("samedi",5),("dimanche",6)]:
                L1[i]["day"]=L1[i]["day"].replace(e[0],e[1])
                date=current_date+datetime.timedelta(days=-1*weekday_number)
                date=current_date+datetime.timedelta(days=L1[i]["day"])
            L1[i]["day"]=date.date().strftime('%m/%d/%Y')
        #if "city" in L[i].keys():
            #L1[i]["city"]=L1[i]["city"][0].upper()+L1[i]["city"][1:]
        if "time" in L[i].keys():
            L1[i]["time"]=L1[i]["time"].replace("heure","h").replace("et","").replace("minute","").replace(":","h").replace("s","").replace(" ","").replace("a","").replace("à","")
    return L1