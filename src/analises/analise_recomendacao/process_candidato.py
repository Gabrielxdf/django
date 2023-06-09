from psycopg2.errors import ProgrammingError
from bd import nova_conexao
from recomendacoes import process_candidato_tfidf, process_candidato_bert

sql_select = "select id, curriculo from emprega_usuario where nivel_usuario = 4"
sql_update = "update emprega_usuario set curriculo_processado = %s, curriculo_embedding = %s where id = %s"

with nova_conexao() as conexao:
    try:
        cursor = conexao.cursor()
        cursor.execute(sql_select)
        curriculos = cursor.fetchall()
    except ProgrammingError as e:
        print(f'Erro: {e.msg}')
    else:
        for row in curriculos:
            cursor.execute(sql_update, (process_candidato_tfidf(
                row[1]), process_candidato_bert(row[1]), row[0]))
        conexao.commit()
