import numpy as np


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
    # a lista perfeita de vagas ordenadas por sua nota
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
