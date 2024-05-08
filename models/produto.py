from .touro import db

class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome_produto = db.Column(db.String(100))
    descricao = db.Column(db.Text)
    preco_unitario = db.Column(db.Numeric(10,2))