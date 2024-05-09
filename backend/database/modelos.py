from appgpt import db

class Conta(db.Model):
    idconta = db.Column(db.Integer, primary_key=True, autoincrement=True)
    usuario = db.Column(db.String(45), nullable=False)
    senha = db.Column(db.String(45), nullable=False)

class Conversa(db.Model):
    idconversa = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome_conversa = db.Column(db.String(45), nullable=False)
    thread = db.Column(db.Text, nullable=True)
    idconta = db.Column(db.Integer, db.ForeignKey('conta.idconta'), nullable=True)
    conta = db.relationship('Conta', backref=db.backref('conversas', lazy=True))

class HistoricoConversa(db.Model):
    idhistorico = db.Column(db.Integer, primary_key=True, autoincrement=True)
    resposta = db.Column(db.Text, nullable=True)
    pergunta = db.Column(db.Text, nullable=True)
    idconversa = db.Column(db.Integer, db.ForeignKey('conversa.idconversa'), nullable=False)
    conversa = db.relationship('Conversa', backref=db.backref('historico', lazy=True))

class Fazenda(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome_fazenda = db.Column(db.String(100))
    estado = db.Column(db.String(50))
    municipio = db.Column(db.String(100))

class Inseminador(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome_inseminador = db.Column(db.String(100))

class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_fazenda = db.Column(db.Integer, db.ForeignKey('fazenda.id'))
    nome_cliente = db.Column(db.String(100))
    email = db.Column(db.String(100))
    telefone = db.Column(db.String(20))
    endereco = db.Column(db.String(200))

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

class Touro(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome_touro = db.Column(db.String(100))
    raca_touro = db.Column(db.String(50))
    empresa_touro = db.Column(db.String(100))

class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome_produto = db.Column(db.String(100))
    descricao = db.Column(db.Text)
    preco_unitario = db.Column(db.Numeric(10,2))

class Vaca(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_fazenda = db.Column(db.Integer, db.ForeignKey('fazenda.id'))
    numero_animal = db.Column(db.Integer)
    lote = db.Column(db.String(50))
    vaca = db.Column(db.String(50))
    categoria = db.Column(db.String(50))
    ECC = db.Column(db.Float)
    ciclicidade = db.Column(db.Integer)

class Venda(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_cliente = db.Column(db.Integer, db.ForeignKey('cliente.id'))
    data_venda = db.Column(db.Date)
    valor_total = db.Column(db.Numeric(10,2))

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

class Visita(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_fazenda = db.Column(db.Integer, db.ForeignKey('fazenda.id'), nullable=False)
    data_visita = db.Column(db.Date, nullable=False)
    fazenda = db.relationship('Fazenda', backref=db.backref('visitas', lazy=True))
