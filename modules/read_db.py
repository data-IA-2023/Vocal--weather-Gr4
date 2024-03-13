from connect2db import *
import pandas as pd



def read_db():
    global conn
    SQL_STATEMENT = """
    SELECT *
    FROM gr4.vocal_weather;
    """
    df=pd.read_sql(SQL_STATEMENT,conn)
    df['entrée_stt'] = df['entrée_stt'].astype("str")
    df['sortie_stt'] = df['sortie_stt'].astype("str")
    df['nlp_loc'] = df['nlp_loc'].astype("str")
    df['nlp_date'] = df['nlp_date'].astype("str")
    df['feedback'] = df['feedback'].astype("str")
    return df