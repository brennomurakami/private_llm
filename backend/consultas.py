import sys
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from appgpt import db
from backend.database.modelos import Conversa, HistoricoConversa, Inseminadores, Fazendas, Clientes, ProtocolosInseminacao, Touros, Vacas, Vendas, ResultadosInseminacao

def processar_sql(mensagem):
    # Extrai o código SQL da mensagem
    codigo_sql = mensagem.split("CODIGO SQL1:")
    codigo_sql = " ".join(codigo_sql).replace("CODIGO SQL1:", "").strip()
    
    # Mantém apenas a parte da string que começa com "SELECT"
    codigo_sql = codigo_sql[codigo_sql.find("SELECT"):]

    # Divide as consultas em partes separadas por "||"
    partes = codigo_sql.split("||")
    print("CONSULTAS: ", partes)

    resultado_final = []

    # Cria uma sessão do SQLAlchemy
    Session = sessionmaker(bind=db.engine)
    session = Session()

    try:
        for parte in partes:
            if parte.strip():
                # Executa cada parte da consulta
                print("EXECUTANDO: ", parte)
                resultado = session.execute(text(parte.strip()))
                print("EXECUTADO")
                print("RESULTADO CONSULTA: ", resultado)

                # Recupere todos os resultados
                rows = resultado.fetchall()

                # Converta as linhas para string
                resultado_lista = '\n'.join([str(row) for row in rows])
                print("RESULTADO: ", resultado_lista)
                
                # Verifica se o resultado está vazio
                if resultado_lista:
                    # Converte o resultado para string e adiciona à lista de resultados finais
                    resultado_final.append('\n'.join([str(a) for a in resultado_lista]))
                else:
                    # Adiciona uma mensagem indicando que não há resultados
                    resultado_final.append("Nenhum resultado encontrado para a consulta: " + parte.strip())

        # Junta todos os resultados em uma única string
        return '\n'.join(resultado_final)

    except Exception as e:
        # Em caso de erro, retorna a mensagem de erro
        print("ERRO")
        return f"Erro ao executar a consulta: {e}"

    finally:
        # Fecha a sessão
        session.close()