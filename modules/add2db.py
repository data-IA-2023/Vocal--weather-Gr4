from connect2db import *

def add2db(weatherFinal):
    """adds the information of weatherFinal to the database"""
    global conn
    def add2db_fct(weatherFinal):
        global conn
        start_stt     = weatherFinal[0]
        entry_request = weatherFinal[1].status_code
        end_stt       = weatherFinal[2]
        locword       = weatherFinal[3]
        locscore      = float(weatherFinal[4])
        dateword      = weatherFinal[5]
        try : datescore = float(weatherFinal[6])
        except : datescore = weatherFinal[6]
        feedback      = weatherFinal[7]

        print(end_stt)
        
        SQL_STATEMENT = """
        INSERT gr4.vocal_weather (
        timestamp, 
        status, 
        entrée_stt, 
        sortie_stt, 
        nlp_loc,
        score_loc,
        nlp_date,
        score_date,
        feedback
        ) OUTPUT INSERTED.id
        VALUES (CURRENT_TIMESTAMP, ?, ?, ?, ?, ?, ?, ?, ?)
        """

        cursor = conn.cursor()
        cursor.execute(
            SQL_STATEMENT,
            entry_request,
            start_stt,
            end_stt.replace('\n',' '),
            locword,
            locscore,
            dateword,
            datescore,
            feedback,
        )
        conn.commit()
    try : add2db_fct(weatherFinal)
    except :
        connect2db()
        add2db_fct(weatherFinal)