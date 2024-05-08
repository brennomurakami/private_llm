from .venda import db

class ResultadoInseminacao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_vaca = db.Column(db.Integer, db.ForeignKey('vaca.id'))
    id_protocolo = db.Column(db.Integer, db.ForeignKey('protocolo_inseminacao.id'))
    id_touro = db.Column(db.Integer, db.ForeignKey('touro.id'))
    id_inseminador = db.Column(db.Integer, db.ForeignKey('inseminador.id'))
    id_venda = db.Column(db.Integer, db.ForeignKey('venda.id'))
    data_inseminacao = db.Column(db.Date)
    numero_IATF = db.Column(db.String(100))
    DG = db.Column(db.Boolean)
    vazia_Com_Ou_Sem_CL = db.Column(db.Boolean)
    perda = db.Column(db.Boolean)