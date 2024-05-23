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

class Endereco(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    rua = db.Column(db.String(100))
    numero = db.Column(db.Integer)
    bairro = db.Column(db.String(100))
    cidade = db.Column(db.String(100))
    estado = db.Column(db.String(2))
    pais = db.Column(db.String(100))

class Fazendas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome_fazenda = db.Column(db.String(100))
    id_endereco = db.Column(db.Integer, db.ForeignKey('endereco.id'))

class Inseminadores(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome_inseminador = db.Column(db.String(100))

class Vendedores(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    cpf = db.Column(db.String(11), unique=True)

class Vacas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_fazenda = db.Column(db.Integer, db.ForeignKey('fazendas.id'))
    numero_animal = db.Column(db.Integer)
    lote = db.Column(db.String(50))
    vaca = db.Column(db.String(50))
    categoria = db.Column(db.String(50))
    ECC = db.Column(db.Float)
    ciclicidade = db.Column(db.Integer)
    peso = db.Column(db.Numeric(10,3))

class Vendas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_fazenda = db.Column(db.Integer, db.ForeignKey('fazendas.id'))
    data_venda = db.Column(db.Date)
    valor_total = db.Column(db.Numeric(10,2))
    id_vendedor = db.Column(db.Integer, db.ForeignKey('vendedores.id'))
    protocolo= db.Column(db.String(100))

class ResultadosInseminacao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_vaca = db.Column(db.Integer, db.ForeignKey('vacas.id'))
    protocolo = db.Column(db.String(100))
    touro = db.Column(db.String(100))
    id_inseminador = db.Column(db.Integer, db.ForeignKey('inseminadores.id'))
    id_venda = db.Column(db.Integer, db.ForeignKey('vendas.id'))
    data_inseminacao = db.Column(db.Date)
    numero_IATF = db.Column(db.String(100))
    DG = db.Column(db.Boolean)
    vazia_Com_Ou_Sem_CL = db.Column(db.Boolean)
    perda = db.Column(db.Boolean)
    venda = db.relationship('Vendas', backref=db.backref('resultados_inseminacao', lazy=True))

class Visitas(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_fazenda = db.Column(db.Integer, db.ForeignKey('fazendas.id'), nullable=False)
    data_visita = db.Column(db.Date, nullable=False)
    id_venda = db.Column(db.Integer, db.ForeignKey('vendas.id'), nullable=True)
    houve_venda = db.Column(db.Boolean)
    id_vendedor = db.Column(db.Integer, db.ForeignKey('vendedores.id'))


