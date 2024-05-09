from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Conta(db.Model):
    idconta = db.Column(db.Integer, primary_key=True, autoincrement=True)
    usuario = db.Column(db.String(45), nullable=False)
    senha = db.Column(db.String(45), nullable=False)
