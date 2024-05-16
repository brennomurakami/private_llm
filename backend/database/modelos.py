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
    id_cliente = db.Column(db.Integer, db.ForeignKey('clientes.id'))
    id_endereco = db.Column(db.Integer, db.ForeignKey('endereco.id'))

class Inseminadores(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome_inseminador = db.Column(db.String(100))

class Clientes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome_cliente = db.Column(db.String(100))
    email = db.Column(db.String(100))
    telefone = db.Column(db.String(20))
    id_endereco = db.Column(db.Integer, db.ForeignKey('endereco.id'))

class ProtocolosInseminacao(db.Model):
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

class Touros(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome_touro = db.Column(db.String(100))
    raca_touro = db.Column(db.String(50))
    empresa_touro = db.Column(db.String(100))

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

class Vendas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_cliente = db.Column(db.Integer, db.ForeignKey('clientes.id'))
    data_venda = db.Column(db.Date)
    valor_total = db.Column(db.Numeric(10,2))
    id_vendedor = db.Column(db.Integer, db.ForeignKey('vendedores.id'))

class ResultadosInseminacao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_vaca = db.Column(db.Integer, db.ForeignKey('vacas.id'))
    id_protocolo = db.Column(db.Integer, db.ForeignKey('protocolos_inseminacao.id'))
    id_touro = db.Column(db.Integer, db.ForeignKey('touros.id'))
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
    fazenda = db.relationship('Fazendas', backref=db.backref('visitas', lazy=True))

class Produtos(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(100))
    quantidade = db.Column(db.Integer)
    touro = db.Column(db.Integer, db.ForeignKey('touros.id'))
    preco = db.Column(db.Numeric(10, 2))
    vendas = db.relationship('Vendas', secondary='item_venda', backref=db.backref('produtos', lazy=True))

class ItemVenda(db.Model):
    vendas_id = db.Column(db.Integer, db.ForeignKey('vendas.id'), primary_key=True)
    produto_id = db.Column(db.Integer, db.ForeignKey('produtos.id'), primary_key=True)
    quantidade = db.Column(db.Integer)
    vendas_relacao = db.relationship('Vendas', backref=db.backref('itens_venda', lazy=True))
    produtos_relacao = db.relationship('Produtos', backref=db.backref('itens_venda', lazy=True))

