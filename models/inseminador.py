from .fazenda import db

class Inseminador(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome_inseminador = db.Column(db.String(100))