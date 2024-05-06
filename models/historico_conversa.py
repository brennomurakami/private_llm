from flask_sqlalchemy import SQLAlchemy
from .conversa import db

class HistoricoConversa(db.Model):
    idhistorico = db.Column(db.Integer, primary_key=True)
    resposta = db.Column(db.Text, nullable=False)
    pergunta = db.Column(db.Text, nullable=False)
    idconversa = db.Column(db.Integer, db.ForeignKey('conversa.idconversa'), nullable=False)
    conversa = db.relationship('Conversa', backref=db.backref('historico', lazy=True))
