from psycopg2.errors import ProgrammingError
from bd import nova_conexao
from recomendacoes import process_vaga_tfidf, process_vaga_bert
import sys

sql_select = "select id, texto from emprega_vaga_analise"
sql_update = "update emprega_vaga_analise set vaga_processada = %s, vaga_embedding = %s where id = %s"

with nova_conexao() as conexao:
    try:
        cursor = conexao.cursor()
        cursor.execute(sql_select)
        vagas = cursor.fetchall()
    except ProgrammingError as e:
        print(f'Erro: {e.msg}')
    else:
        for row in vagas:
            cursor.execute(sql_update, (process_vaga_tfidf(
                row[1]), process_vaga_bert(row[1], sys.argv[1], sys.argv[2]), row[0]))
        conexao.commit()