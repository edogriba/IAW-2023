import sqlite3

def get_foto():
    query = "SELECT * FROM FOTO_ANNUNCI"
    conn = sqlite3.connect("db/RenTo.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results

def get_foto_by_id_annuncio(id_annuncio):
    query = "SELECT * FROM FOTO_ANNUNCI WHERE id_annuncio == ? ORDER BY indice_foto"
    conn = sqlite3.connect("db/RenTo.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(query, (id_annuncio,))
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results

def get_foto_by_id_utente(id_utente):
    query = "SELECT indice_foto, FOTO_ANNUNCI.id_annuncio, url_immagine FROM FOTO_ANNUNCI, ANNUNCI WHERE FOTO_ANNUNCI.id_annuncio == ANNUNCI.id_annuncio AND id_utente == ? ORDER BY FOTO_ANNUNCI.id_annuncio, indice_foto"
    conn = sqlite3.connect("db/RenTo.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(query, (id_utente,))
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results

def inserisci_foto_indice(id_annuncio, indice_foto, url_immagine):
    insert = "INSERT INTO FOTO_ANNUNCI (id_annuncio, indice_foto, url_immagine) VALUES (?, ?, ?)"
    conn = sqlite3.connect("db/RenTo.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    success = False
    print(id_annuncio, indice_foto, url_immagine)
    try:
        cursor.execute(insert, (id_annuncio, indice_foto, url_immagine))
        conn.commit()
        success = True
        print(insert, success)
    except Exception as e:
        print('Error: ', str(e))
        conn.rollback()
    cursor.close()
    conn.close()
    return success

def cancella_foto_indice(id_annuncio, indice_foto):
    delete = "DELETE FROM FOTO_ANNUNCI WHERE id_annuncio == ? AND indice_foto == ?"
    conn = sqlite3.connect("db/RenTo.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    success = False
    print(id_annuncio, indice_foto)
    try:
        cursor.execute(delete, (id_annuncio, indice_foto))
        conn.commit()
        success = True
        print(delete, success)

    except Exception as e:
        print('Error: ', str(e))
        conn.rollback()
    cursor.close()
    conn.close()
    return success

def sostituisci_foto_indice(id_annuncio, indice_foto, nuovo_url_immagine):
    update = "UPDATE FOTO_ANNUNCI SET url_immagine = ? WHERE id_annuncio == ? AND indice_foto == ?"
    conn = sqlite3.connect("db/RenTo.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    success = False
    print(nuovo_url_immagine, id_annuncio, indice_foto)
    try:
        cursor.execute(update, (nuovo_url_immagine, id_annuncio, indice_foto))
        conn.commit()
        success = True
        print(update, success)
    except Exception as e:
        print('Error: ', str(e))
        conn.rollback()
    cursor.close()
    conn.close()
    return success

def get_numero_foto_annuncio(id_annuncio):
    query = "SELECT COUNT(*) AS numero_foto FROM FOTO_ANNUNCI where id_annuncio == ? "
    conn = sqlite3.connect("db/RenTo.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(query, (id_annuncio,))
    results = cursor.fetchone()
    cursor.close()
    conn.close()
    return results

def get_max_indice(id_annuncio):
    query = "SELECT MAX(indice_foto) AS max FROM FOTO_ANNUNCI WHERE id_annuncio == ? "
    conn = sqlite3.connect("db/RenTo.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(query, (id_annuncio,))
    results = cursor.fetchone()
    cursor.close()
    conn.close()
    return results