from .protocolos_inseminacao import db

class Touro(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome_touro = db.Column(db.String(100))
    raca_touro = db.Column(db.String(50))
    empresa_touro = db.Column(db.String(100))