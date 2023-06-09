from psycopg2.errors import ProgrammingError
from bd import nova_conexao
import numpy as np


def get_notas():
    sql_select_notas = "select usuario_id, vaga_id, nota from nota order by usuario_id, vaga_id"
    #são 20 currículos/usuários e 35 vagas
    notas = np.zeros((20,35), dtype=int)

    with nova_conexao() as conexao:
        try:
            cursor = conexao.cursor()
            cursor.execute(sql_select_notas)
            resultado = cursor.fetchall()
        except ProgrammingError as e:
            print(f'Erro: {e.msg}')
        else:
            for row in resultado:
                notas[row[0]-1][row[1]-1] = row[2] #-1 porque os id's começam com 1
            conexao.commit()
    return notas


def get_vagas_ordenadas():
    #obtém as vagas ordenadas por notas
    sql_select_vagas_ordenadas = "select row_number() over(order by usuario_id, nota desc), * from nota"
    #são 20 currículos/usuários e 35 vagas
    vagas = np.zeros((20,35), dtype=int)

    with nova_conexao() as conexao:
        try:
            cursor = conexao.cursor()
            cursor.execute(sql_select_vagas_ordenadas)
            resultado = cursor.fetchall()
        except ProgrammingError as e:
            print(f'Erro: {e.msg}')
        else:
            for row in resultado:
                vagas[row[1]-1][34 if row[0]%35 == 0 else (row[0]%35)-1] = row[2]-1 #-1 porque os id's dos usuários começam com 1
            conexao.commit()
    return vagas