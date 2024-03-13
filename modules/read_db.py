from connect2db import *



def read_db():
    global conn
    SQL_STATEMENT = """
    FROM gr4.vocal_weather
    SELECT *;
    """