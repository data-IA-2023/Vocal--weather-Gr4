import re
import pickle
import os
import copy
from datapackage import Package

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

cities_pattern = re.compile('^'+'|^'.join(cities)+'|'+'| '.join(cities))

info_pattern= r"météo|température|pluie|((beau|mauvais)( |-))?temps"

relative_date_pattern= r"demain|aujourd('| )hui|après(-| )demain|hier|avant( |-)hier|(dans |(il )?y ?a )?([0-9]|une?|deux|trois|quatres?|cinq|six|sept|huit|neuf|dix) (jours?|semaines?|mois)( dans le (futur|passé))?"

time_pattern=r"(dans |(il )?y ?a )?((([0-1][0-9]|2[0-3])(:| ?h| ?H)[0-5][0-9])|([0-1][0-9]|2[0-3]) ?(heures( et)?|(et)?)?( ?(([0-5][0-9]|[0-9])( minutes?)?|(( |-)(demi|quart))|(moins( |-)quart)))?)"

def match_pattern(pattern,text):
    match=re.search(pattern, text)
    if match:
        return match.group()
    return ""

def extract_features(text):
    global date_pattern,cities_pattern,info_pattern,relative_day_pattern,time_pattern
    patterns={"date":date_pattern,"city":cities_pattern,"info":info_pattern,"relative_date":relative_date_pattern,"time":time_pattern}
    features={}
    for pattern in patterns.keys():
        match=match_pattern(patterns[pattern],text.lower())
        if match != "":
            if match[-1] in [" ","?",",",".",":",";"] : features[pattern]=match[:-1]
            else : features[pattern]=match
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