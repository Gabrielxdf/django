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
            nltk.download('stopwords', quiet=True)
            stopwords_list = stopwords.words('english') + stopwords.words('portuguese')
            vectorizer = TfidfVectorizer(stop_words=stopwords_list)
            corpus_tfidf = vectorizer.fit(todas_vagas)
        for row_c in curriculos:
            for row_v in vagas:
                vaga_tfidf = corpus_tfidf.transform([row_v[1]])
                curriculo_tfidf = corpus_tfidf.transform([row_c[1]])
                cosine_similarities = cosine_similarity(curriculo_tfidf, vaga_tfidf)
                print(cosine_similarities)
            break