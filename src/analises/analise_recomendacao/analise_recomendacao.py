from psycopg2.errors import ProgrammingError
from bd import nova_conexao
import recomendacoes as r
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import os
import nltk
from sklearn.metrics.pairwise import cosine_similarity

sql_select_curriculo = "select id, curriculo_processado from emprega_usuario \
    where nivel_usuario = 4 order by id"
sql_select_vaga = "select id, vaga_processada from emprega_vaga order by id"

with nova_conexao() as conexao:
    try:
        cursor = conexao.cursor()
        cursor.execute(sql_select_curriculo)
        curriculos = cursor.fetchall()
        cursor.execute(sql_select_vaga)
        vagas = cursor.fetchall()
    except ProgrammingError as e:
        print(f'Erro: {e.msg}')
    else:
        todas_vagas=[]
        for row in vagas:
            todas_vagas.append(row[1])
        for row_c in curriculos:
            resultado_vagas, resultado_indices = r.recommend_vagas_tfidf(todas_vagas, [row_c[1]])
            print(resultado_indices)
            break