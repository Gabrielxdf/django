from psycopg2.errors import ProgrammingError
from bd import nova_conexao
import recomendacoes as r
import numpy as np
from select_notas_2 import get_notas, get_vagas_ordenadas


def average_precision(usuario_id, documentos_relevancia, notas_reais):
    predicoes_relevantes = 0
    soma = 0
    for i, id_doc in enumerate(documentos_relevancia, start=1):
        if notas_reais[usuario_id][id_doc] > 3: #se o doc é relevante
            predicoes_relevantes += 1
            soma = soma + predicoes_relevantes/i
    if predicoes_relevantes == 0:
        average_precision = 1.0
    else:
        average_precision = soma/predicoes_relevantes
    return average_precision


def mean_average_precision(usuario_resultado_relevancia, notas_reais):
    map = []
    for usuario_id, resultado_vagas in enumerate(usuario_resultado_relevancia):
        map.append(average_precision(usuario_id, resultado_vagas, notas_reais))
    return np.mean(map)


def dcg(usuario_resultado_relevancia, notas_reais):
    dcg = []
    dcg_final = []
    for usuario_id, resultado_vagas in enumerate(usuario_resultado_relevancia):
        for i, id_vaga in enumerate(resultado_vagas, start=1):
            numerador = (2 ** notas_reais[usuario_id][id_vaga])-1
            denominador = np.log2((i)+1)
            dcg.append(numerador/denominador)
        dcg_final.append(sum(dcg))
    return dcg_final


def idcg(notas_reais):
    #a lista perfeita de vagas ordenadas por sua nota
    vagas_id_ordenadas = [np.argsort(notas)[::-1] for notas in notas_reais]
    idcg = []
    idcg_final = []
    for usuario_id, resultado_vagas in enumerate(vagas_id_ordenadas):
        for i, id_vaga in enumerate(resultado_vagas, start=1):
            numerador = (2 ** notas_reais[usuario_id][id_vaga])-1
            denominador = np.log2((i)+1)
            idcg.append(numerador/denominador)
        idcg_final.append(sum(idcg))
    return idcg_final


def ndcg(usuario_resultado_relevancia, notas_reais):
    resultado_dcg = dcg(usuario_resultado_relevancia, notas_reais)
    resultado_idcg = idcg(notas_reais)
    return np.mean(np.array(resultado_dcg)/np.array(resultado_idcg))


if __name__ == '__main__':
    sql_select_curriculo = "select id, curriculo_processado, curriculo_embedding from \
        emprega_usuario_analise order by id"
    sql_select_vaga = "select id, vaga_processada, vaga_embedding from emprega_vaga_analise order by id"
    notas_reais = get_notas()
    usuario_resultado_relevancia_tfidf = []
    usuario_resultado_relevancia_bert = []
    usuario_resultado_relevancia_concatenacao= []
    tempo_tfidf = []
    tempo_bert = []
    tempo_concatenado = []

    with nova_conexao() as conexao:
        try:
            cursor = conexao.cursor()
            cursor.execute(sql_select_curriculo)
            curriculos = cursor.fetchall()
            cursor.execute(sql_select_vaga)
            vagas_tfidf, vagas_bert = zip(*[(row[1], row[2]) for row in cursor.fetchall()])
        except ProgrammingError as e:
            print(f'Erro: {e.msg}')
        else:
            for row in curriculos:
                resultado_vagas_tfidf, resultado_indices_tfidf, time_tfidf = \
                r.recommend_vagas_tfidf(vagas_tfidf, [row[1]])
                usuario_resultado_relevancia_tfidf.append(resultado_indices_tfidf)
                tempo_tfidf.append(time_tfidf)

                resultado_vagas_bert, resultado_indices_bert,time_bert = \
                    r.recommend_vagas_bert(vagas_bert, row[2])
                usuario_resultado_relevancia_bert.append(resultado_indices_bert)
                tempo_bert.append(time_bert)

                resultado_vagas_conc, resultado_indices_conc, time_conc = \
                    r.recommend_vagas_concatenacao(vagas_tfidf, [row[1]], vagas_bert, row[2])
                usuario_resultado_relevancia_concatenacao.append(resultado_indices_conc)
                tempo_concatenado.append(time_conc)

    resultado_map_tfidf = mean_average_precision(usuario_resultado_relevancia_tfidf, notas_reais)
    resultado_map_bert = mean_average_precision(usuario_resultado_relevancia_bert, notas_reais)
    resultado_map_concatenacao = mean_average_precision(usuario_resultado_relevancia_concatenacao, notas_reais)
    resultado_ndcg_tfidf = ndcg(usuario_resultado_relevancia_tfidf, notas_reais)
    resultado_ndcg_bert = ndcg(usuario_resultado_relevancia_bert, notas_reais)
    resultado_ndcg_concatenacao = ndcg(usuario_resultado_relevancia_concatenacao, notas_reais)
    
    print(f'As similaridades com o TF-IDF foram calculadas com o tempo médio de: {np.mean(tempo_tfidf, dtype=np.float16)}s')
    print(f'As similaridades com o BERT foram calculadas com o tempo médio de: {np.mean(tempo_bert, dtype=np.float16)}s')
    print(f'As similaridades com a CONCATENAÇÃO foram calculadas com o tempo médio de: {np.mean(tempo_concatenado, dtype=np.float16)}s')
    print(f'MAP da recomendação de vagas usando TF-IDF: {resultado_map_tfidf}')
    print(f'MAP da recomendação de vagas usando BERT: {resultado_map_bert}')
    print(f'MAP da recomendação de vagas usando CONCATENAÇÃO: {resultado_map_concatenacao}')
    print(f'NDCG da recomendação de vagas usando TF-IDF: {resultado_ndcg_tfidf}')
    print(f'NDCG da recomendação de vagas usando BERT: {resultado_ndcg_bert}')
    print(f'NDCG da recomendação de vagas usando CONCATENAÇÃO: {resultado_ndcg_concatenacao}')