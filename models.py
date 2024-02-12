from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, id, nome, cognome, email, password, immagine_profilo, tipo_utente):
        self.id= id
        self.nome = nome
        self.cognome = cognome
        self.email = email
        self.password = password
        self.immagine_profilo = immagine_profilo
        self.tipo_utente = tipo_utente