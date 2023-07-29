from psycopg2.errors import ProgrammingError
from bd import nova_conexao
from recomendacoes import process_vaga_tfidf, process_vaga_bert
import sys

sql_select = "select vag.id, vag.cargo || ' ' || vag.atividades || ' ' || vag.requisitos \
    || ' ' || emp.ramo_atividade || ' ' || emp.descricao from emprega_vaga vag \
    inner join emprega_empresa emp on vag.empresa_id = emp.id"
sql_update = "update emprega_vaga set vaga_processada = %s, vaga_embedding = %s where id = %s"

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
                row[1]), process_vaga_bert(row[1]), sys.argv[1] if sys.argv[1] != None else "", row[0]))
        conexao.commit()