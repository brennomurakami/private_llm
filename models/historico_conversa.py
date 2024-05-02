from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from .conversa import db

class HistoricoConversa(db.Model):
    idhistorico = db.Column(db.Integer, primary_key=True)
    mensagem = db.Column(db.Text, nullable=False)
    pergunta = db.Column(db.Boolean, nullable=False)
    data_hora = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    idconversa = db.Column(db.Integer, db.ForeignKey('conversa.idconversa'), nullable=False)
    conversa = db.relationship('Conversa', backref=db.backref('historico', lazy=True))
