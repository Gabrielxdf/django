import os
import time
import pandas as pd
import PyPDF2
import nltk
import fitz
import numpy as np
from nltk.corpus import stopwords
from sentence_transformers import SentenceTransformer, models
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from unidecode import unidecode

def get_pdf_text_2(pdf_path):
    media_path = os.path.join(os.path.dirname(__file__), '../curriculos')
    pdf_path = os.path.join(media_path, pdf_path)

    reader = fitz.open(pdf_path)
    text = []

    for page in reader:
        text.append(page.get_text())

    text = " ".join(text).replace("\n", "")

    return text

def process_candidato_tfidf(curriculo):
    # o caminho do currículo vai no parâmetro
    text = get_pdf_text_2(str(curriculo))

    text = treat_text(text)
    return text


def process_vaga_tfidf(vaga_text):
    vaga_text = treat_text(vaga_text)

    return vaga_text


def recommend_vagas_concatenacao(vagas_tfidf, user_tfidf, vagas_bert, user_bert):
    start = time.time()

    user_text = [str(user_tfidf)]
    vagas_text = [str(vaga) for vaga in vagas_tfidf]
    user_embedding = [user_bert]
    vagas_embedding = [vaga for vaga in vagas_bert]

    # curriculo tfidf, vagas tfidf
    query_tfidf, corpus_tfidf, vectorizer = apply_tfidf(user_text, vagas_text)
    cosine_similarities_tfidf = cosine_similarity(query_tfidf, corpus_tfidf)
    cosine_similarities_bert = cosine_similarity(user_embedding, vagas_embedding)
    cosine_similarities_concatenado = (np.array(cosine_similarities_tfidf[0]) +
                                       np.array(cosine_similarities_bert[0])) / 2.0

    indexes = np.argsort(cosine_similarities_concatenado)[::-1]
    queries = list(np.array(list(vagas_tfidf))[indexes])

    timer = time.time() - start

    return queries, indexes, timer


def recommend_vagas_tfidf(vagas, user):
    start = time.time()

    user_text = [str(user)]
    vagas_text = [str(vaga) for vaga in vagas]

    # curriculo tfidf, vagas tfidf
    query_tfidf, corpus_tfidf, vectorizer = apply_tfidf(user_text, vagas_text)
    cosine_similarities = cosine_similarity(query_tfidf, corpus_tfidf)
    
    indexes = np.argsort(cosine_similarities[0])[::-1]
    queries = list(np.array(list(vagas))[indexes])

    timer = time.time() - start

    # exportar a matriz tf-idf para xlsx
    df = pd.DataFrame(corpus_tfidf.toarray(),
                      columns=vectorizer.get_feature_names_out())
    #df.to_excel(os.path.abspath("src/analises/analise_recomendacao/recomendar_vagas/corpus_tfidf.xlsx"), encoding='utf-8', index=False)

    # exportar a matriz tf-idf para xlsx
    df = pd.DataFrame(query_tfidf.toarray(),
                      columns=vectorizer.get_feature_names_out())
    #df.to_excel(os.path.abspath("src/analises/analise_recomendacao/recomendar_vagas/query_tfidf.xlsx"), encoding='utf-8', index=False)

    return queries, indexes, timer


def recommend_candidatos_tfidf(candidatos, vaga):
    start = time.time()

    vaga_text = [str(vaga)]
    candidatos_text = [str(candidato) for candidato in candidatos]

    # vaga_tfidf, curriculos_tfidf
    query_tfidf, corpus_tfidf, vectorizer = apply_tfidf(vaga_text, candidatos_text)
    # retorna um vetor com as similaridades da vaga com todos os currículos
    cosine_similarities = cosine_similarity(query_tfidf, corpus_tfidf)

    # np.argsort() retorna os índices que ordenariam esse vetor, e o [::-1] apenas vai inverter esse vetor
    # de índices para obter o índice de maior resultado, para o índice de menor.
    indexes = np.argsort(cosine_similarities[0])[::-1]

    # queries nesse caso são os candidatos, estou criando uma nova lista de candidatos usando os índices obtidos
    # dos melhores resultados para os piores
    queries = list(np.array(list(candidatos))[indexes])

    print(f'tfidf + cosine = {time.time() - start}')

    # exportar a matriz tf-idf para xlsx
    df = pd.DataFrame(corpus_tfidf.toarray(),
                      columns=vectorizer.get_feature_names_out())
    #df.to_excel(os.path.abspath("src/analises/analise_recomendacao/recomendar_candidatos/corpus_tfidf.xlsx"), encoding='utf-8', index=False)

    # exportar a matriz tf-idf para xlsx
    df = pd.DataFrame(query_tfidf.toarray(),
                      columns=vectorizer.get_feature_names_out())
    #df.to_excel(os.path.abspath("src/analises/analise_recomendacao/recomendar_candidatos/query_tfidf.xlsx"), encoding='utf-8', index=False)

    return queries


def get_pdf_text(pdf_path):
    media_path = os.path.join(os.path.dirname(__file__), '../curriculos')
    pdf_path = os.path.join(media_path, pdf_path)

    reader = PyPDF2.PdfReader(pdf_path)
    text = []

    for page in reader.pages:
        text.append(page.extract_text())

    text = " ".join(text)

    return text


def treat_text(text):
    nltk.download('rslp', quiet=True)
    stemmer = nltk.stem.RSLPStemmer()
    text = text.lower().strip(" ").split(" ")
    text = " ".join([stemmer.stem(word) for word in text if word != ''])
    text = unidecode(str(text))

    return text


def apply_tfidf(query, corpus):
    nltk.download('stopwords', quiet=True)
    stopwords_list = stopwords.words('english') + stopwords.words('portuguese')

    vectorizer = TfidfVectorizer(stop_words=stopwords_list)

    corpus_tfidf = vectorizer.fit_transform(corpus)
    query_tfidf = vectorizer.transform(query)

    return query_tfidf, corpus_tfidf, vectorizer


def load_bert_model(model_name="paraphrase-multilingual-MiniLM-L12-v2", pooling_method="mean"):
    #paraphrase-multilingual-MiniLM-L12-v2
    #neuralmind/bert-base-portuguese-cased
    #neuralmind/bert-large-portuguese-cased
    #unicamp-dl/ptt5-base-portuguese-vocab
    #unicamp-dl/ptt5-large-portuguese-vocab
    #xlm-roberta-base
    #xlm-roberta-large
    model_path = os.path.join(os.path.dirname(
        __file__), f'bert_models/{model_name}')

    try:
        model = SentenceTransformer(model_path, device="cpu")
    except ValueError:
        print("Model not found in local directory")
        model = SentenceTransformer(model_name, device="cpu")
        model.save(model_path)
        print(f'Model saved at {model_path}')
    finally:
        model._modules["1"].pooling_mode_mean_tokens = True if pooling_method == "mean" else False
        model._modules["1"].pooling_mode_max_tokens = True if pooling_method == "max" else False
        model._modules["1"].pooling_mode_cls_token = True if pooling_method == "cls" else False
        model._modules["1"].pooling_mode_mean_sqrt_len_tokens = True if pooling_method == "mean_sqrt" else False
        #model._modules["0"].max_seq_length = 512
        print(f'\nMODELO {model_name} COM POOLING {pooling_method}')
        print(model._modules["1"])

        return model


def process_candidato_bert(curriculo, model_name="paraphrase-multilingual-MiniLM-L12-v2", pooling_method="mean"):
    model = load_bert_model(model_name, pooling_method)
    text = get_pdf_text_2(str(curriculo))

    embedding = model.encode(text, show_progress_bar=False).tolist()

    return embedding


def process_vaga_bert(text, model_name="paraphrase-multilingual-MiniLM-L12-v2", pooling_method="mean"):
    model = load_bert_model(model_name, pooling_method)

    embedding = model.encode(text, show_progress_bar=False).tolist()

    return embedding


def recommend_vagas_bert(vagas, user):
    start = time.time()

    user_embedding = [user]
    vagas_embedding = [vaga for vaga in vagas]

    cosine_similarities = cosine_similarity(user_embedding, vagas_embedding)

    indexes = np.argsort(cosine_similarities[0])[::-1]
    queries = list(np.array(list(vagas))[indexes])

    timer = time.time() - start

    return queries, indexes, timer


def recommend_candidatos_bert(candidatos, vaga):
    start = time.time()

    vaga_embedding = [vaga]
    candidatos_embedding = [candidato for candidato in candidatos]

    cosine_similarities = cosine_similarity(
        vaga_embedding, candidatos_embedding)

    indexes = np.argsort(cosine_similarities[0])[::-1]
    queries = list(np.array(list(candidatos))[indexes])

    print(f'bert + cosine = {time.time() - start}')

    return queries


if __name__ == '__main__':
    from django.apps import apps

    Usuario = apps.get_model('emprega.Usuario')
    Vaga = apps.get_model('emprega.Vaga')

    usuarios = Usuario.objects.filter(nivel_usuario=4)
    vagas = Vaga.objects.all()
    usuario = Usuario.objects.get(cpf="13673179675")
    vaga = Vaga.objects.get(pk=1)

    vagas_rec = recommend_vagas_bert(vagas, usuario)
    candidatos_rec = recommend_candidatos_bert(usuarios, vaga)

    print(vagas_rec, candidatos_rec)
