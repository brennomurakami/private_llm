from .cliente import db

class ProtocoloInseminacao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    protocolo = db.Column(db.String(100))
    dias_protocolo = db.Column(db.Integer)
    implante_P4 = db.Column(db.String(100))
    empresa = db.Column(db.String(100))
    GnRH_NA_IA = db.Column(db.Boolean)
    PGF_NO_D0 = db.Column(db.Integer)
    dose_PGF_retirada = db.Column(db.Numeric(10,2))
    marca_PGF_retirada = db.Column(db.String(100))
    dose_CE = db.Column(db.Numeric(10,2))
    eCG = db.Column(db.String(100))
    dose_eCG = db.Column(db.Numeric(10,2))