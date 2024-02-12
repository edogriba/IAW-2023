import sqlite3

def get_prenotazioni_by_utente(id_utente):
    query = "SELECT id_prenotazione, data, orario, stato, tipo_visita, motivazione, PRENOTAZIONI.id_annuncio, nome, cognome, email, immagine_profilo, titolo, indirizzo FROM PRENOTAZIONI, UTENTI, ANNUNCI WHERE PRENOTAZIONI.id_annuncio == ANNUNCI.id_annuncio AND ANNUNCI.id_utente == UTENTI.id_utente AND PRENOTAZIONI.id_utente == ? ORDER BY PRENOTAZIONI.id_annuncio, id_prenotazione"
    conn = sqlite3.connect("db/RenTo.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(query, (id_utente,))
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results

def utente_gia_prenotato(id_utente, id_annuncio):
    query = "SELECT stato FROM PRENOTAZIONI WHERE id_utente == ? AND id_annuncio == ? AND (stato == 'accettata' OR stato == 'richiesta')"
    conn = sqlite3.connect("db/RenTo.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(query, (id_utente, id_annuncio))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result

def get_orari_occupati(id_annuncio):
    query = "SELECT data, orario FROM PRENOTAZIONI WHERE id_annuncio == ? AND stato == 'accettata' ORDER BY data, orario"
    conn = sqlite3.connect("db/RenTo.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(query, (id_annuncio,))
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results

def data_orario_disponibili(prenotazione):
    query = "SELECT COUNT(*) AS numero_prenotazioni_accettate FROM PRENOTAZIONI WHERE data == ? AND orario == ? AND id_annuncio == ? AND stato == 'accettata'"
    conn = sqlite3.connect("db/RenTo.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(query, (str(prenotazione['data']), str(prenotazione['orario']), prenotazione['id_annuncio']))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result

def inserisci_prenotazione(prenotazione, id_utente):
    insert = "INSERT INTO PRENOTAZIONI (stato, data, orario, tipo_visita, id_annuncio, id_utente) VALUES (?,?,?,?,?,?)"
    conn = sqlite3.connect("db/RenTo.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    success = False
    try:
        cursor.execute(insert, (prenotazione['stato'], prenotazione['data'], prenotazione['orario'], prenotazione['tipo_visita'], prenotazione['id_annuncio'], id_utente))
        conn.commit()
        success = True
    except Exception as e:
        print('Error: ', str(e))
        conn.rollback()
    cursor.close()
    conn.close()
    return success

def get_prenotazioni_by_annuncio(id_annuncio):
    query = "SELECT id_prenotazione, PRENOTAZIONI.id_annuncio, data, orario, stato, tipo_visita, motivazione, nome, cognome, email, immagine_profilo, titolo, indirizzo FROM PRENOTAZIONI, UTENTI, ANNUNCI WHERE PRENOTAZIONI.id_annuncio == ANNUNCI.id_annuncio AND PRENOTAZIONI.id_utente == UTENTI.id_utente AND ANNUNCI.id_annuncio == ? ORDER BY data DESC, id_prenotazione DESC"
    conn = sqlite3.connect("db/RenTo.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(query, (id_annuncio,))
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results

def modifica_prenotazione( tipo_modifica, id_prenotazione, motivazione):
    update = "UPDATE PRENOTAZIONI SET stato = ?, motivazione = ? WHERE id_prenotazione == ? "
    conn = sqlite3.connect("db/RenTo.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    success = False
    try:
        cursor.execute(update, (tipo_modifica, motivazione, id_prenotazione,))
        conn.commit()
        success = True
    except Exception as e:
        print('Error: ', str(e))
        conn.rollback()
    cursor.close()
    conn.close()
    return success

def get_date_accettate_richieste(id_utente, id_annuncio):
    query = "SELECT data FROM PRENOTAZIONI WHERE id_utente == ? AND id_annuncio = ? AND (stato == 'accettata' OR stato == 'richiesta') ORDER BY orario"
    conn = sqlite3.connect("db/RenTo.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(query, (id_utente, id_annuncio) )
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results