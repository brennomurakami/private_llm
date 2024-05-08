from .inseminador import db

class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_fazenda = db.Column(db.Integer, db.ForeignKey('fazenda.id'))
    nome_cliente = db.Column(db.String(100))
    email = db.Column(db.String(100))
    telefone = db.Column(db.String(20))
    endereco = db.Column(db.String(200))