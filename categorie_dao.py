import sqlite3

def get_categorie():
    query = "SELECT * FROM CATEGORIE"
    conn = sqlite3.connect("db/RenTo.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(query, )
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results