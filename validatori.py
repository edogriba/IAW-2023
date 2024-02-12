from datetime import datetime, timedelta
from flask import Flask, flash

ESTENSIONI_CONSENTITE = {'png', 'jpg', 'jpeg'}

def file_consentito(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ESTENSIONI_CONSENTITE

def valida_dizionario(dizionario):
    success = True
    for key in dizionario.keys():
        if not dizionario[key] or dizionario[key].isspace():
            success = False
            flash('Il campo ' + str(key)+ ' del form era vuoto', 'danger') 
    return success  

def valida_annuncio(annuncio):
    success = True
    success = valida_dizionario(annuncio)
    try:
        if float(annuncio['prezzo_mensile']) < 1:
            success = False
            flash('Il prezzo non può essere un numero negativo', 'danger')

    except Exception:
        success = False
        flash('Il prezzo non è un numero reale', 'danger')
    if not (3 <= len(str(annuncio['titolo'])) <= 50 ):
        success = False
        flash('Il titolo deve avere tra i 3 e i 50 caratteri')
    if not (5 <= len(str(annuncio['indirizzo'])) <= 40 ):
        success = False
        flash('L\'indirizzo deve avere tra i 5 e i 40 caratteri')
    if not (10 <= len(str(annuncio['descrizione'])) <= 350 ):
        success = False
        flash('La descrizione deve avere tra i 10 e i 350 caratteri')
    try:
        if int(annuncio['disponibile']) != 0 and int(annuncio['disponibile']) != 1:
            success = False
            flash('La disponibilità ha un formato sconosciuto', 'danger')
    except Exception:
        success = False
        flash('La disponibilità ha un formato sconosciuto', 'danger')
    try:
        if int(annuncio['arredata']) != 0 and int(annuncio['arredata']) != 1:
            success = False
            flash('L\'arredamento ha un formato sconosciuto', 'danger')
    except Exception:
        success = False
        flash('L\'arredamento ha un formato sconosciuto', 'danger')
    try:    
        if not annuncio['numero_locali'].isdigit():
            success =  False
            flash('Il numero di locali ha un formato sconosciuto', 'danger')
    except Exception:
        success =  False
        flash('Il numero di locali ha un formato sconosciuto', 'danger')
    try:
        if not annuncio['categoria_casa'].isdigit():
            success =  False
            flash('La categoria della casa ha un formato sconosciuto', 'danger')
    except Exception:
        success =  False
        flash('La categoria della casa ha un formato sconosciuto', 'danger')

    return success

def valida_prenotazione(prenotazione):
    success = True
    success = valida_dizionario(prenotazione)
    if prenotazione['data'] < str(datetime.now()) or prenotazione['data'] > str(datetime.now()+ timedelta(days=7)):
        success = False
        flash('La data non è valida', 'danger')
    if prenotazione['tipo_visita'] != 'persona' and prenotazione['tipo_visita'] != 'remoto':
        success = False
        flash('Il tipo di visita ha un formato sconosciuto', 'danger')
    if prenotazione['orario'] != '9-12' and prenotazione['orario'] != '12-14' and prenotazione['orario'] != '14-17' and prenotazione['orario'] != '17-20':
        success = False
        flash('L\'ora ha un formato sconosciuto', 'danger')
    return success

def valida_motivazione_rifiuto(motivazione):
    if motivazione == "" or motivazione == " ":
        return False
    if len(motivazione) < 6:
        flash('La motivazione deve essere lunga almeno 6 caratteri', 'danger')
        return False
    elif len(motivazione) > 100 :
        flash('La motivazione deve essere lunga meno di 100 caratteri', 'danger')
        return False
    else:
        return True
    
def valida_modifiche(annuncio):
    success = True
    for key in annuncio.keys():
        if annuncio[key] == "" or annuncio[key]== " " :
            success = False
            flash('Il campo ' + str(key)+ ' del form era vuoto', 'danger')
    try:
        float(annuncio['prezzo_mensile'])
    except Exception as e:
        success = False
        flash('Il prezzo non è un numero reale', 'danger')
    if not (4 <= len(str(annuncio['titolo'])) <= 50 ):
        success = False
        flash('Il titolo deve avere tra i 4 e i 50 caratteri', 'danger')
    try:
        value = int(annuncio['disponibile'])
        if value != 0 and value != 1:
            success = False
            flash('La disponibilità ha un formato sconosciuto', 'danger')
    except Exception:
        success = False
        flash('La disponibilità ha un formato sconosciuto', 'danger')
    try:
        value = int(annuncio['arredata'])
        if value != 0 and value != 1:
            success = False
            flash('L\'arredamento ha un formato sconosciuto', 'danger')
    except Exception:
        success = False
        flash('L\'arredamento ha un formato sconosciuto', 'danger')
    try:
        value = int(annuncio['numero_locali'])
        if not ( 1 <= int(annuncio['numero_locali']) <= 5) :
            success =  False
            flash('Il numero di locali ha un formato sconosciuto', 'danger')
    except Exception:
        success = False
        flash('Il numero di locali ha un formato sconosciuto', 'danger')

    try:
        value = int(annuncio['categoria_casa'])
        if not ( 0 <= int(annuncio['categoria_casa']) <= 3) :
            success =  False
            flash('La categoria della casa ha un formato sconosciuto', 'danger')
    except Exception:
        success = False
        flash('La categoria della casa ha un formato sconosciuto', 'danger')
    
    return success

def valida_nuovo_utente(nuovo_utente):
    
    success = valida_dizionario(nuovo_utente)
    
    if not (2 <= len(str(nuovo_utente['nome'])) <= 25 ):
        success = False
        flash('Il nome deve avere tra i 2 e i 25 caratteri', 'danger')
    if not (2 <= len(str(nuovo_utente['cognome'])) <= 30 ):
        success = False
        flash('Il cognome deve avere tra i 2 e i 30 caratteri', 'danger')
    # lunghezza minima della password per questioni di sicurezza
    if not (len(str(nuovo_utente['password'])) > 3):
        success = False
        flash('La password deve avere almeno 4 caratteri', 'danger')
    try:
        if nuovo_utente['tipo_utente'] != 'Locatario' and nuovo_utente['tipo_utente'] != 'Cliente':
            success = False
            flash('Il tipo utente ha un formato sconosciuto', 'danger')
    except Exception:
        success = False
        flash('Il tipo utente ha un formato sconosciuto', 'danger')

    return success