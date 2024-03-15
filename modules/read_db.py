from connect2db import *
import pandas as pd



def read_db():
    """reads the database and returns a pandas dataframe"""
    global conn
    def read_db_fct():
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
    try :
        r=read_db_fct()
        return r
    except :
        connect2db()
        return read_db_fct()
