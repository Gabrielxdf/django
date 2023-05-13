from psycopg2.errors import ProgrammingError
from bd import nova_conexao
from recomendacao.recommendation import get_pdf_text

sql_select = "select id, curriculo from emprega_usuario where nivel_usuario = 4"
sql_update = "update emprega_usuario set curriculo_texto = %s where id = %s"

with nova_conexao() as conexao:
    try:
        cursor = conexao.cursor()
        cursor.execute(sql_select)
        curriculos = cursor.fetchall()
    except ProgrammingError as e:
        print(f'Erro: {e.msg}')
    else:
        for row in curriculos:
            cursor.execute(sql_update, (get_pdf_text(str(row[1])), row[0]))
        conexao.commit()
