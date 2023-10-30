from psycopg2.errors import ProgrammingError
from bd import nova_conexao
import os
import fitz
from pathlib import Path
#import sys
#sys.path.append("..")

sql_select = "select id, curriculo from emprega_usuario_analise"
sql_update = "update emprega_usuario_analise set curriculo_texto = %s where id = %s"

with nova_conexao() as conexao:
    try:
        cursor = conexao.cursor()
        cursor.execute(sql_select)
        curriculos = cursor.fetchall()
    except ProgrammingError as e:
        print(f'Erro: {e.msg}')
    else:
        for row in curriculos:
            diretório = './analises/curriculos/'
            curriculo_path = os.path.join(diretório, row[1])
            text = []
            reader = fitz.open(curriculo_path)
            for page in reader:
                text.append(page.get_text())
            text = " ".join(text).replace("\n", " ")            
            cursor.execute(sql_update, (text, row[0]))
        conexao.commit()
