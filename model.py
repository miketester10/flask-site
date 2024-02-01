from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, id, nome, cognome, username, matricola, email, password):
        self.id = id
        self.nome = nome
        self.cognome = cognome
        self.username = username
        self.matricola = matricola
        self.email = email
        self.password = password