import sqlite3

def get_utenti():
    query = "SELECT * FROM UTENTI"
    conn = sqlite3.connect("db/RenTo.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results

def crea_utente(nuovo_utente):
    insert = "INSERT INTO UTENTI (nome, cognome, email, password, immagine_profilo, tipo_utente) VALUES (?, ?, ?, ?, ?, ?)"
    conn = sqlite3.connect("db/RenTo.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    success = False
    try:
        cursor.execute(insert, (nuovo_utente['nome'], nuovo_utente['cognome'], nuovo_utente['email'], nuovo_utente['password'], nuovo_utente['immagine_profilo'], nuovo_utente['tipo_utente']))
        conn.commit()
        success = True
    except Exception as e:
        print('Error', str(e))
        conn.rollback()
    cursor.close()
    conn.close()
    return success

def get_utente_by_id(utente_id):
    query = "SELECT * FROM UTENTI WHERE id_utente == ?"
    conn = sqlite3.connect("db/RenTo.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(query, (utente_id,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result

def cerca_utente_by_email(email):
    query = "SELECT * FROM UTENTI WHERE email == ?"
    conn = sqlite3.connect("db/RenTo.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    result = None
    try:
        cursor.execute(query, (email,))
        result = cursor.fetchone()
    except Exception as e:
        print('Error', str(e))
    cursor.close()
    conn.close()
    return result

def cambia_immagine_profilo(immagine_profilo, id_utente):
    update = "UPDATE UTENTI SET immagine_profilo = ? WHERE id_utente == ? "
    conn = sqlite3.connect("db/RenTo.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    success = False
    try:
        cursor.execute(update, (immagine_profilo, id_utente))
        conn.commit()
        success = True
    except Exception as e:
        print('Error: ', str(e))
        conn.rollback()
    cursor.close()
    conn.close()
    return success