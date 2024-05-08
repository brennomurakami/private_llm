from .produto import db

class Vaca(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_fazenda = db.Column(db.Integer, db.ForeignKey('fazenda.id'))
    numero_animal = db.Column(db.Integer)
    lote = db.Column(db.String(50))
    vaca = db.Column(db.String(50))
    categoria = db.Column(db.String(50))
    ECC = db.Column(db.Float)
    ciclicidade = db.Column(db.Integer)