from contextlib import contextmanager
from psycopg2 import connect

parametros = dict(user="empregaanapolis",
                  password="empregaanapolis",
                  host="127.0.0.1",
                  port="5432",
                  database="empregaanapolis")


@contextmanager
def nova_conexao():
    conexao = connect(**parametros)
    try:
        yield conexao
    finally:
        if (conexao and conexao.closed):
            conexao.close()
