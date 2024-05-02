from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from .conta import db

class Conversa(db.Model):
    idconversa = db.Column(db.Integer, primary_key=True)
    nome_conversa = db.Column(db.String(45), nullable=False)
    data = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    idconta = db.Column(db.Integer, db.ForeignKey('conta.idconta'), nullable=False)
    conta = db.relationship('Conta', backref=db.backref('conversas', lazy=True))
