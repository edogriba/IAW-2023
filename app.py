# Importazioni dei moduli utili per la web app
from flask import Flask, render_template, url_for, redirect, request, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

# Importazioni della libreria secrets per creare nomi unici per le immagini uploadate
import secrets
# Importazioni della libreria datetime per gestire le date
from datetime import datetime, timedelta

# Importazione di moduli per imolementare controlli di sicurezza
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

# Importazioni dei file dao con le funzioni per interagire con il database
import annunci_dao
import utenti_dao
import foto_dao 
import prenotazioni_dao
import categorie_dao

# Importazione del file con il template dell'utente
import models

# Importazione di funzione per validare gli input
import validatori



# Creazione dell'applicazione 

app = Flask(__name__)
app.config['SECRET_KEY'] = '!P4ssW0rD!'
login_manager = LoginManager()
login_manager.init_app(app)


# Definizione delle route principali

@app.route('/')
def start():
    return render_template('start.html')

@app.route('/home/<int:filter>')
def home(filter):
    if not filter or filter is None:
        annunci = annunci_dao.get_annunci()
    else:
        annunci = annunci_dao.get_annunci_by_nlocali()
    foto = foto_dao.get_foto()
    return render_template('home.html', annunci=annunci, foto=foto, filter=filter)

@app.route('/annunci/<int:id_annuncio>')
def mostra_annuncio(id_annuncio):
    foto = foto_dao.get_foto_by_id_annuncio(id_annuncio)
    annuncio = annunci_dao.get_annuncio_by_id(id_annuncio)
    locatario = utenti_dao.get_utente_by_id(annuncio['id_utente']) # questo è il locatario dell'annuncio ( le info mi servono per mostrare una card con la foto profilo e qualche informazione)
    if current_user.is_authenticated and locatario['id_utente'] != current_user.id: # si cerca se c'è una prenotazione sulla casa solo se l'utente è autenticato e non è il locatario della casa
        id_utente = int(current_user.id)
        prenotazione = prenotazioni_dao.utente_gia_prenotato(id_utente, id_annuncio) # ce ne può essere solo una perchè c'è la WHERE clause con prenotazione richiesta o accettata, infatti nella funzione faccio fetchone()
    else:
        prenotazione = None
    giorni_limite = []
    # così creo i 7 giorni successivi per la prenotazione
    giorni_limite.append((datetime.now()+ timedelta(days=1)).strftime("%Y-%m-%d"))
    giorni_limite.append((datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d"))

    return render_template('annuncio.html', annuncio=annuncio, foto=foto, locatario=locatario, giorni_limite=giorni_limite, prenotazione=prenotazione)

# Gestione inserimento e modifica di un annuncio 

@app.route('/annunci/crea_annuncio')
@login_required
def crea_annuncio():
    categorie = categorie_dao.get_categorie()
    return render_template('crea_annuncio.html', categorie=categorie)

@app.route('/annunci/nuovo_annuncio', methods=['POST'])
@login_required
def nuovo_annuncio():
    if current_user.tipo_utente == 'Locatario':
        annuncio = request.form.to_dict()
        success_foto = 0
        general_success = True
        # valido i dati ricevuti dal form 
        success_annuncio = validatori.valida_annuncio(annuncio)
        # se i dati sono validi allora creo l'annuncio
        if success_annuncio:
            id_annuncio = annunci_dao.inserisci_annuncio(annuncio, int(current_user.id))
        # se ho creato correttamente l'annuncio inserisco tutte le foto che caricate nel form
        if id_annuncio:
            for i in range(5):
                foto = request.files.get('img-aggiunta-' + str(i))
                if foto and foto.filename and validatori.file_consentito(foto.filename):
                    foto.filename = secure_filename(foto.filename)
                    # per creare una stringa unica come nome dell'immagine si usa una combinazione del timestamp
                    # preso con precisione fino al millisecondo e una stringa random 
                    tempo = datetime.utcnow().strftime('%Y%m%d%H%M%S%f')[:-3]  
                    stringa_random = secrets.token_hex(4)
                    nuovo_url_immagine = tempo + stringa_random + foto.filename
                    foto.save('static/immagini/' + nuovo_url_immagine)
                    success_foto = foto_dao.inserisci_foto_indice(id_annuncio, i, nuovo_url_immagine)
                    if not success_foto:
                        general_success = False
                    else:
                        success_foto = success_foto + 1 # così conto le volte che si è avuto successo con il caricamento di una foto

        if success_annuncio and success_foto  == 0: # se nemmeno una foto è stata caricata bisogna cancellare l'ultimo annuncio inserito perchè non rispetta le condizioni di avere 1-5 foto
            annunci_dao.cancella_annuncio(max)
            flash('Annuncio non creato. Devi inserire almeno una foto', 'danger')
            return redirect(url_for('crea_annuncio'))
        elif success_annuncio and general_success:
            flash('Annuncio inserito correttamente', 'success')
            return redirect(url_for('home', filter=0))
        elif success_annuncio and not general_success and success_foto > 0: # se si è avuto successo nel caricamento dell'annuncio e  si è riuscito caricare almeno una delle fotol'annuncio viene comunque creato ma viene flashato un warning
            flash('Annuncio creato. Problema nell\'inserimento di 1 o più foto dell\'annuncio', 'warning')
            return redirect(url_for('home', filter=0))
        else:
            flash('Annuncio non creato. Problema nell\'inserimento dell\'annuncio', 'danger')
            return redirect(url_for('crea_annuncio'))
    else:
        return redirect(url_for('home', filter=0))

@app.route('/annunci/<int:id_annuncio>/modifica_annuncio/', methods=['POST'])
@login_required
def modifica_annuncio(id_annuncio):
    if current_user.tipo_utente == 'Locatario':
        modifiche = request.form.to_dict()
        success_modifiche = validatori.valida_modifiche(modifiche)
        if success_modifiche:
            success_modifiche = annunci_dao.inserisci_modifiche(modifiche, id_annuncio)
        
        success_foto = True

        for i in range(5):
            # ogni riga vedo se c'è un'immagine aggiunta o un'immagine da cancellare o un'immagine da sostituire
            try:
                aggiunta = request.files['img-aggiunta-' + str(id_annuncio) + '-' + str(i)]
                cancellazione = ''
                sostitutiva = ''
            except Exception:
                aggiunta = ''
                cancellazione = ('cancellazione-' + str(id_annuncio) + '-' + str(i))
                sostitutiva = request.files['img-sostitutiva-' + str(id_annuncio) + '-' + str(i)]

            if aggiunta != '' and aggiunta.filename:
                if  validatori.file_consentito(aggiunta.filename): 
                    aggiunta.filename = secure_filename(aggiunta.filename)
                    # per creare una stringa unica come nome dell'immagine si usa una combinazione del timestamp
                    # preso con precisione fino al millisecondo e una stringa random 
                    tempo = datetime.utcnow().strftime('%Y%m%d%H%M%S%f')[:-3]  
                    stringa_random = secrets.token_hex(4)
                    nuovo_url_immagine = tempo + stringa_random + aggiunta.filename
                    aggiunta.save('static/immagini/' + nuovo_url_immagine)
                    success = foto_dao.inserisci_foto_indice(id_annuncio, i, nuovo_url_immagine)
                    if not success:
                            success_foto = False
                            flash('Fallimento nell\'inserimento della foto numero ' + str(i) , 'danger')
                else:
                    success_foto = False
                    flash('Nome foto numero ' + str(i+1) + ' potenzialmente pericoloso', 'danger')
            elif cancellazione != '' or sostitutiva != '':   # se non è stata aggiunta l'immagine vedo se è da cancellare
                if modifiche[cancellazione] == str(1):
                    if foto_dao.get_numero_foto_annuncio(id_annuncio)['numero_foto'] == 1:
                        messaggio = "Foto numero " + str(i+1) + " non cancellata. L'annuncio deve avere almeno una foto"
                        flash(messaggio, 'warning')
                        success_foto = False
                    else:
                        success = foto_dao.cancella_foto_indice(id_annuncio, i)
                        if not success:
                            success_foto = False
                            messaggio = "Fallimento nella cancellazione della foto numero " + str(i+1)
                            flash(messaggio, 'danger')
                else:
                    if sostitutiva != '' and sostitutiva.filename: 
                        if  validatori.file_consentito(sostitutiva.filename):   
                            filename = secure_filename(sostitutiva.filename)
                            # per creare una stringa unica come nome dell'immagine si usa una combinazione del timestamp
                            # preso con precisione fino al millisecondo e una stringa random 
                            tempo = datetime.utcnow().strftime('%Y%m%d%H%M%S%f')[:-3]  
                            stringa_random = secrets.token_hex(4)
                            nuovo_url_immagine = tempo + stringa_random + filename
                            sostitutiva.save('static/immagini/' + nuovo_url_immagine)
                            success = foto_dao.sostituisci_foto_indice(id_annuncio, i, nuovo_url_immagine)
                            if not success:
                                success_foto = False
                                messaggio = "Fallimento nella sostituzione della foto numero " + str(i+1)
                                flash(messaggio, 'danger')            
                        else:
                            success_foto = False
                            flash('Nome foto numero ' + str(i+1) + ' potenzialmente pericoloso', 'danger')
    else:
        flash('L\'utente deve essere un locatario', 'danger')   
    if success_modifiche and success_foto:
        flash('Annuncio modificato con successo', 'success')
    else:
        flash('Problema con modifica dell\'annuncio', 'warning')

    return redirect(url_for('mieiannunci'))

# Gestione del profilo

@app.route('/profilo/mieidati')
@login_required
def mieidati():
    return render_template('mieidati.html')

@app.route('/profilo/mieidati/cambia_immagine_profilo', methods=['POST'])
@login_required
def cambia_immagine_profilo():

    foto = request.files.get('img-sostitutiva-profilo')
    success = False
    if foto and foto.filename and validatori.file_consentito(foto.filename):
        foto.filename = secure_filename(foto.filename)
        # per creare una stringa unica come nome dell'immagine si usa una combinazione del timestamp
        # preso con precisione fino al millisecondo e una stringa random 
        timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S%f')[:-3]  
        random_string = secrets.token_hex(4)
        foto.save('static/immagini/' + timestamp + random_string + foto.filename)
        immagine_profilo = timestamp + random_string + foto.filename
        success = utenti_dao.cambia_immagine_profilo(immagine_profilo, int(current_user.id))
        if not success:
            flash('Problema nell\'inserimento dell\'immagine', 'danger')
    else:
        flash('Url dell\'immagine non valida', 'danger')
    if not success:
        flash('Immagine del profilo non modificata', 'danger')
    return redirect(url_for('mieidati'))

@app.route('/profilo/mieiannunci')
@login_required
def mieiannunci():
    id_utente = int(current_user.id)
    annunci = annunci_dao.get_annunci_by_utente(id_utente)
    foto = foto_dao.get_foto_by_id_utente(id_utente)
    categorie = categorie_dao.get_categorie()
    annunci_disponibili = []
    annunci_non_disponibili = []
    for annuncio in annunci:
        if annuncio['disponibile']:
            annunci_disponibili.append(annuncio)
        else:
            annunci_non_disponibili.append(annuncio)

    prenotazioni = []
    for annuncio in annunci:
        for prenotazione in prenotazioni_dao.get_prenotazioni_by_annuncio(annuncio['id_annuncio']):
            prenotazioni.append(prenotazione)

    return render_template('mieiannunci.html', annunci_disponibili=annunci_disponibili, annunci_non_disponibili=annunci_non_disponibili, foto=foto, prenotazioni=prenotazioni, categorie=categorie)

@app.route('/profilo/prenotazioni_effettuate')
@login_required
def prenotazioni_effettuate():
    prenotazioni = prenotazioni_dao.get_prenotazioni_by_utente(int(current_user.id))
    return render_template('prenotazioni_effettuate.html', prenotazioni=prenotazioni)

# Gestione richieste di prenotazioni

@app.route('/nuova_prenotazione/<int:id_annuncio>', methods=['POST'])
@login_required
def nuova_prenotazione(id_annuncio):

    # verifica lato server se l'utente ha già una prenotazione

    stato = prenotazioni_dao.utente_gia_prenotato(current_user.id, id_annuncio)
    if stato:
        if stato['stato'] == 'richiesta' or stato['stato'] == 'accettata':
            flash('Prenotazione non effettuata. L\'utente ha già una prenotazione ' + str(stato), 'danger')
            return redirect(url_for('mostra_annuncio', id_annuncio=id_annuncio))

    prenotazione = request.form.to_dict()

    # validazione del form della prenotazione

    success = validatori.valida_prenotazione(prenotazione)

    if not success:
        return redirect(url_for('mostra_annuncio', id_annuncio=id_annuncio)) 

    prenotazione['stato'] = 'richiesta'
    prenotazione['id_annuncio'] = id_annuncio

    # controllo che non ci siano altre prenotazioni accettate alla stessa data e stessa ora

    result = prenotazioni_dao.data_orario_disponibili(prenotazione)

    numero_prenotazioni = result['numero_prenotazioni_accettate']

    # se c'è già una prenotazione accettata a quell'ora non permetto la prenotazione e flasho un messaggio che dice che non si può effettuare la prenotazione a quell'ora

    if numero_prenotazioni > 0:
        flash('Prenotazione non effettuata. La fascia oraria selezionata non è disponibile. Provare con un\'altra fascia', 'danger')
        return redirect(url_for('mostra_annuncio', id_annuncio=id_annuncio))
    
    # se invece il programma continua (non è entrato nell'if precedente) allora posso inserire la prenotazione

    success = prenotazioni_dao.inserisci_prenotazione(prenotazione, int(current_user.id))

    if success:
        flash('Prenotazione richiesta con successo', 'success')
    else:
        flash('Prenotazione non riuscita, problema con l\'inserimento della prenotazione', 'danger')

    # in ogni caso reindirizzo sempre alla pagina dell'annuncio

    return redirect(url_for('mostra_annuncio', id_annuncio=id_annuncio))

@app.route('/accetta_prenotazione/<int:id_prenotazione>')
@login_required
def accetta_prenotazione(id_prenotazione):

    motivazione = None
    
    success = prenotazioni_dao.modifica_prenotazione('accettata', id_prenotazione, motivazione) 

    if success:
        flash('Prenotazione accettata con successo', 'success')
    else:
        flash('Modifica dello stato della prenotazione fallita ', 'danger')
    
    return redirect(url_for('mieiannunci'))

@app.route('/rifiuta_prenotazione/<int:id_prenotazione>', methods=['POST'])
@login_required
def rifiuta_prenotazione(id_prenotazione):
    
    motivazione = request.form['motivazione']

    success  = validatori.valida_motivazione_rifiuto(motivazione)
    
    if not success:
        flash('Modifica della prenotazione fallita. Il campo motivazione non era valido', 'danger')
        return redirect(url_for('mieiannunci'))

    success = prenotazioni_dao.modifica_prenotazione('rifiutata', id_prenotazione, motivazione) 

    if success:
        flash('Prenotazione rifiutata con successo', 'success')
    else:
        flash('Modifica dello stato della prenotazione fallita ', 'danger')
    
    return redirect(url_for('mieiannunci'))


# Gestione iscrizione

@app.route('/iscriviti')
def iscriviti():
    return render_template('iscriviti.html')
@app.route('/iscrizione', methods=['POST'])
def iscrizione():

    nuovo_utente = request.form.to_dict()
    
    success = validatori.valida_nuovo_utente(nuovo_utente)
    if not success:
        flash('Iscrizione non riuscita', 'danger')
        return redirect('iscriviti')

    foto = request.files.get('immagine_profilo')

    if foto and foto.filename and validatori.file_consentito(foto.filename):
        foto.filename = secure_filename(foto.filename)
        # per creare una stringa unica come nome dell'immagine si usa una combinazione del timestamp
        # preso con precisione fino al millisecondo e una stringa random 
        timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S%f')[:-3]  
        random_string = secrets.token_hex(4)
        foto.save('static/immagini/' + timestamp + random_string + foto.filename)
        nuovo_utente['immagine_profilo'] = timestamp + random_string + foto.filename
    else:
        nuovo_utente['immagine_profilo'] = 'user.jpg'

    
    nuovo_utente['password'] = generate_password_hash(nuovo_utente['password'])

    result = utenti_dao.crea_utente(nuovo_utente)

    if not result:
        flash('Email associata ad un altro account. Registrazione fallita.', 'danger')
        return redirect(url_for('iscriviti'))
    
    flash('Registrazione avvenuta con successo', 'success')
    return redirect(url_for('home', filter=0))

# Gestione login e logout

@login_manager.user_loader
def load_user(id_utente):
    db_utente = utenti_dao.get_utente_by_id(id_utente)
    user = models.User( id=db_utente['id_utente'], nome=db_utente['nome'], cognome=db_utente['cognome'], email=db_utente['email'], password=db_utente['password'], immagine_profilo=db_utente['immagine_profilo'], tipo_utente=db_utente['tipo_utente'])
    return user

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/nuovologin', methods=['POST'])
def newlogin():
    utente = request.form.to_dict()
    
    utente_db = utenti_dao.cerca_utente_by_email(utente['email'])
    if not utente_db or not check_password_hash(utente_db['password'], utente['password']):
        flash('Email e/o password non valide', 'danger')
        return redirect(url_for('login'))
    else:
        new = models.User(id=utente_db['id_utente'], nome=utente_db['nome'], cognome=utente_db['cognome'], email=utente_db['email'], password=utente_db['password'], immagine_profilo=utente_db['immagine_profilo'], tipo_utente=utente_db['tipo_utente'])
        login_user(new, True)
        print('Success!')
        flash('Hai effettuato il login con successo!', 'success')
        return redirect(url_for('home', filter=0))
    
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Hai effettuato il logout con successo!', 'info')
    return redirect(url_for('home', filter=0))
