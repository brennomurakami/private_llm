from .historico_conversa import db

class Fazenda(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome_fazenda = db.Column(db.String(100))
    estado = db.Column(db.String(50))
    municipio = db.Column(db.String(100))