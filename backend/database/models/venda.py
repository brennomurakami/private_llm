from .vaca import db

class Venda(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_cliente = db.Column(db.Integer, db.ForeignKey('cliente.id'))
    data_venda = db.Column(db.Date)
    valor_total = db.Column(db.Numeric(10,2))