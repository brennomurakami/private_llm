import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from appgpt import db
from backend.database.modelos import Conversa, HistoricoConversa, Inseminador, Fazenda, Cliente, ProtocoloInseminacao, Touro, Produto, Vaca, Venda, ResultadoInseminacao

# Função para retornar o total de vendas e a média de vendas por período específico
def total_vendas_periodo(inicio, fim):
    print("ENTROU")
    print(inicio)
    print(fim)
    total_vendas = Venda.query.filter(Venda.data_venda.between(inicio, fim)).with_entities(db.func.sum(Venda.valor_total).label('total_vendas')).first()
    media_vendas = Venda.query.filter(Venda.data_venda.between(inicio, fim)).with_entities(db.func.avg(Venda.valor_total).label('media_vendas')).first()
    print(total_vendas)
    print(media_vendas)
    return total_vendas, media_vendas

# Função para retornar os clientes que fizeram o maior número de compras ou geraram o maior volume de vendas
def maiores_clientes():
    query = db.session.query(Cliente.nome_cliente, db.func.count(Venda.id).label('total_compras')).join(Venda).group_by(Cliente.id).order_by(db.desc('total_compras')).limit(5)
    return query.all()

# Função para retornar o protocolo de inseminação mais utilizado
def protocolo_mais_utilizado():
    query = db.session.query(ProtocoloInseminacao.protocolo, db.func.count(ResultadoInseminacao.id_protocolo).label('total_utilizado')).join(ResultadoInseminacao).group_by(ProtocoloInseminacao.id).order_by(db.desc('total_utilizado')).first()
    return query

# Função para retornar o touro mais utilizado nos procedimentos de inseminação
def touro_mais_utilizado():
    query = db.session.query(Touro.nome_touro, db.func.count(ResultadoInseminacao.id_touro).label('total_utilizado')).join(ResultadoInseminacao).group_by(Touro.id).order_by(db.desc('total_utilizado')).first()
    return query

# Função para calcular o percentual de vacas que não engravidaram após o procedimento de inseminação
def percentual_erro():
    total_vacas = Vaca.query.count()
    vacas_sem_gestacao = ResultadoInseminacao.query.filter_by(perda=True).count()
    percentual = (vacas_sem_gestacao / total_vacas) * 100
    return percentual

def obter_resultados_inseminacao_ordenados_por_data():
    print("FUNCAO ATIVADA: obter_resultados_inseminacao_ordenados_por_data")
    resultados = db.session.query(
        ResultadoInseminacao.id.label('id_resultado'),
        ResultadoInseminacao.data_inseminacao,
        Fazenda.nome_fazenda.label('fazenda'),
        Inseminador.nome_inseminador.label('inseminador'),
        Vaca.numero_animal,
        Vaca.vaca,
        Touro.nome_touro,
        ProtocoloInseminacao.protocolo,
        ResultadoInseminacao.numero_IATF,
        db.case((ResultadoInseminacao.DG == 1, 'Sim'), else_='Não').label('prenha'),
        db.case((ResultadoInseminacao.vazia_Com_Ou_Sem_CL == 1, 'Com CL'), else_='Sem CL').label('status_gestacional'),
        db.case((ResultadoInseminacao.perda == 1, 'Sim'), else_='Não').label('perda_gestacional')
    ).join(
        Vaca, ResultadoInseminacao.id_vaca == Vaca.id
    ).join(
        Fazenda, Vaca.id_fazenda == Fazenda.id
    ).join(
        ProtocoloInseminacao, ResultadoInseminacao.id_protocolo == ProtocoloInseminacao.id
    ).join(
        Touro, ResultadoInseminacao.id_touro == Touro.id
    ).join(
        Inseminador, ResultadoInseminacao.id_inseminador == Inseminador.id
    ).order_by(
        ResultadoInseminacao.data_inseminacao.desc()
    ).all()

    return resultados

def formular_resposta(mensagem):
    print(mensagem)
    # Lista de todas as funções disponíveis
    funcoes_disponiveis = {
        "total_vendas_periodo": total_vendas_periodo,
        "maiores_clientes": maiores_clientes,
        "protocolo_mais_utilizado": protocolo_mais_utilizado,
        "touro_mais_utilizado": touro_mais_utilizado,
        "percentual_erro": percentual_erro,
        "obter_resultados_inseminacao_ordenados_por_data": obter_resultados_inseminacao_ordenados_por_data
    }

    # Verifica se a mensagem contém a solicitação direta para as funções necessárias
    if "FUNCOES NECESSARIAS:" in mensagem:
        # Remove a parte "FUNCOES NECESSARIAS:" da mensagem
        mensagem = mensagem.replace("FUNCOES NECESSARIAS:", "").strip()

        # Inicializa uma lista para armazenar os resultados
        resultados = []

        # Verifica se o nome da função está presente na mensagem e chama a função correspondente
        for funcao_nome, funcao in funcoes_disponiveis.items():
            if funcao_nome in mensagem:
                parametros = None
                # Verifica se há parâmetros na mensagem
                if 'total_vendas_periodo' in funcao_nome:
                    parametros_str = mensagem[mensagem.find("(") + 1: mensagem.find(")")]
                    parametros = parametros_str.split(",")
                # Chama a função sem parâmetros se não houver argumentos na mensagem
                resultado = funcao() if not parametros else funcao(*parametros)
                resultados.append((funcao_nome, resultado))

        # Gera a resposta no formato solicitado
        resposta = " ".join([f"Função {funcao}: Resultado {resultado}" for funcao, resultado in resultados])

    else:
        # Se a resposta direta foi fornecida, atribui diretamente à resposta
        resposta = mensagem

    return resposta
