import sqlite3

def get_annunci():
    query = "SELECT * FROM ANNUNCI, CATEGORIE WHERE id_categoria == categoria_casa AND disponibile == 1 ORDER BY prezzo_mensile DESC"
    conn = sqlite3.connect("db/RenTo.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results

def get_annunci_by_nlocali():
    query = "SELECT * FROM ANNUNCI, CATEGORIE WHERE id_categoria == categoria_casa AND disponibile == 1 ORDER BY numero_locali"
    conn = sqlite3.connect("db/RenTo.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results

def get_annunci_by_utente(id_utente):
    query = "SELECT * FROM ANNUNCI, CATEGORIE WHERE id_utente == ? AND id_categoria == categoria_casa ORDER BY prezzo_mensile DESC"
    conn = sqlite3.connect("db/RenTo.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(query, (id_utente,))
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results

def get_annuncio_by_id(id_annuncio):
    query = "SELECT * FROM ANNUNCI, CATEGORIE WHERE id_annuncio == ? AND id_categoria == categoria_casa"
    conn = sqlite3.connect("db/RenTo.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(query, (id_annuncio,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result

def inserisci_modifiche(modifiche, id_annuncio):
    update = "UPDATE ANNUNCI SET titolo = ?, descrizione = ?, categoria_casa = ?, numero_locali = ?, prezzo_mensile = ?, disponibile = ?, arredata = ? WHERE id_annuncio == ? "
    conn = sqlite3.connect("db/RenTo.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    success = False
    try:
        cursor.execute(update, (modifiche['titolo'], modifiche['descrizione'], modifiche['categoria_casa'], modifiche['numero_locali'], modifiche['prezzo_mensile'], modifiche['disponibile'], modifiche['arredata'], id_annuncio))
        conn.commit()
        success = True
    except Exception as e:
        print('Error: ', str(e))
        conn.rollback()
    cursor.close()
    conn.close()
    return success

def inserisci_annuncio(annuncio, id_utente):
    insert = "INSERT INTO ANNUNCI (titolo, indirizzo, descrizione, categoria_casa, numero_locali, prezzo_mensile, disponibile, arredata, id_utente) VALUES (?,?,?,?,?,?,?,?,?)"
    conn = sqlite3.connect("db/RenTo.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    success = False
    try:
        cursor.execute(insert, (annuncio['titolo'], annuncio['indirizzo'], annuncio['descrizione'], annuncio['categoria_casa'], annuncio['numero_locali'], annuncio['prezzo_mensile'], annuncio['disponibile'], annuncio['arredata'], id_utente ))
        conn.commit()
        success = True
    except Exception as e:
        print('Error: ', str(e))
        conn.rollback()
    if success:
        query =  "SELECT last_insert_rowid()"
        cursor.execute(query)
        result = cursor.fetchone()
    cursor.close()
    conn.close()
    if success:
        return result
    return success

def get_max_id_annuncio():
    query = "SELECT MAX(id_annuncio) AS max FROM ANNUNCI"
    conn = sqlite3.connect("db/RenTo.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(query,)
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result

def cancella_annuncio(id_annuncio):
    delete = "DELETE FROM ANNUNCI WHERE id_annuncio == ?"
    conn = sqlite3.connect("db/RenTo.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    try:
        cursor.execute(delete, (id_annuncio, ))
        conn.commit()
    except Exception as e:
        print('Error: ', str(e))
        conn.rollback()
    cursor.close()
    conn.close()