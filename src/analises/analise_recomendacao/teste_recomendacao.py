import recomendacoes as r
import os

curriculo_dev_texto = r.process_candidato_tfidf(
    '../curriculos/curriculo_ciencia_computacao_1.pdf')
curriculo_dev_embedding = r.process_candidato_bert(
    '../curriculos/curriculo_ciencia_computacao_1.pdf')

curriculo_bio_texto = r.process_candidato_tfidf(
    '../curriculos/curriculo_biologia_1.pdf')
curriculo_bio_embedding = r.process_candidato_bert(
    '../curriculos/curriculo_biologia_1.pdf')

vaga_dev_texto = r.process_vaga_tfidf("Desenvolvedor Full-Stack Desenvolver aplicações web e mobile utilizando as tecnologias mais modernas do mercado. Trabalhar em equipe para a entrega de soluções de alta qualidade e performance. Participar de reuniões de planejamento e definir as melhores abordagens para as demandas do projeto. Experiência prévia em desenvolvimento de software. Conhecimento em tecnologias como React, Node.js, SQL, MongoDB, entre outras. Ensino superior completo ou em andamento em áreas relacionadas. Boa comunicação e habilidades interpessoais. Cinematográfo Environmental use seek happen his glass. Blood yard street heavy listen relationship. Office month agreement should. Physical popular Mr trade important city better then.")
vaga_dev_embedding = r.process_vaga_bert("Desenvolvedor Full-Stack Desenvolver aplicações web e mobile utilizando as tecnologias mais modernas do mercado. Trabalhar em equipe para a entrega de soluções de alta qualidade e performance. Participar de reuniões de planejamento e definir as melhores abordagens para as demandas do projeto. Experiência prévia em desenvolvimento de software. Conhecimento em tecnologias como React, Node.js, SQL, MongoDB, entre outras. Ensino superior completo ou em andamento em áreas relacionadas. Boa comunicação e habilidades interpessoais. Cinematográfo Environmental use seek happen his glass. Blood yard street heavy listen relationship. Office month agreement should. Physical popular Mr trade important city better then.")

vaga_marketing_texto = r.process_vaga_tfidf("Assistente de Marketing Auxiliar nas atividades de marketing, incluindo criação de campanhas publicitárias, planejamento e execução de eventos e promoções, produção de conteúdo para mídias sociais e outros canais de comunicação. Acompanhar métricas e resultados das ações de marketing. Experiência prévia em atividades de marketing. Conhecimento em mídias sociais, produção de conteúdo e ferramentas de marketing digital. Formação em Marketing, Publicidade e Propaganda ou áreas afins. Habilidade em criatividade, trabalho em equipe e bom relacionamento interpessoal. Cinematográfo Environmental use seek happen his glass. Blood yard street heavy listen relationship. Office month agreement should. Physical popular Mr trade important city better then.")
vaga_marketing_embedding = r.process_vaga_bert("Assistente de Marketing Auxiliar nas atividades de marketing, incluindo criação de campanhas publicitárias, planejamento e execução de eventos e promoções, produção de conteúdo para mídias sociais e outros canais de comunicação. Acompanhar métricas e resultados das ações de marketing. Experiência prévia em atividades de marketing. Conhecimento em mídias sociais, produção de conteúdo e ferramentas de marketing digital. Formação em Marketing, Publicidade e Propaganda ou áreas afins. Habilidade em criatividade, trabalho em equipe e bom relacionamento interpessoal. Cinematográfo Environmental use seek happen his glass. Blood yard street heavy listen relationship. Office month agreement should. Physical popular Mr trade important city better then.")

vaga_farmacia_texto = r.process_vaga_tfidf("Farmacêutico Realizar atendimento ao cliente em farmácias, orientando sobre o uso de medicamentos e produtos de saúde. Realizar controle de estoque e dispensação de medicamentos. Participar de processos de manipulação e produção de medicamentos. Experiência prévia em atendimento farmacêutico. Formação em Farmácia e registro no Conselho Regional de Farmácia. Conhecimento em legislação sanitária, gestão de estoque e dispensação de medicamentos. Habilidade em comunicação, atendimento ao cliente e trabalho em equipe. Metalúrgico About amount write collection respond. Raise treat now future fact much protect. Region design city. Everyone poor value democratic.")
vaga_farmacia_embedding = r.process_vaga_bert("Farmacêutico Realizar atendimento ao cliente em farmácias, orientando sobre o uso de medicamentos e produtos de saúde. Realizar controle de estoque e dispensação de medicamentos. Participar de processos de manipulação e produção de medicamentos. Experiência prévia em atendimento farmacêutico. Formação em Farmácia e registro no Conselho Regional de Farmácia. Conhecimento em legislação sanitária, gestão de estoque e dispensação de medicamentos. Habilidade em comunicação, atendimento ao cliente e trabalho em equipe. Metalúrgico About amount write collection respond. Raise treat now future fact much protect. Region design city. Everyone poor value democratic.")

resultado_vaga_tfidf = r.recommend_vagas_tfidf(
    list((vaga_marketing_texto, vaga_dev_texto)), curriculo_dev_texto)
resultado_vaga_bert = r.recommend_vagas_bert(
    list((vaga_marketing_embedding, vaga_dev_embedding)), curriculo_dev_embedding)
print(resultado_vaga_tfidf)

resultado_curriculo_tfidf = r.recommend_candidatos_tfidf(
    list((curriculo_bio_texto, curriculo_dev_texto)), vaga_farmacia_texto)
resultado_curriculo_bert = r.recommend_candidatos_bert(list(
    (curriculo_bio_embedding, curriculo_dev_embedding)), vaga_farmacia_embedding)
print(resultado_curriculo_tfidf)


with open(os.path.abspath('src/analises/recomendacao/vagas.txt'), 'r') as file:
    lista_vagas = file.readlines()

resultado_vaga_tfidf = r.recommend_vagas_tfidf(
    lista_vagas, curriculo_dev_texto)
print(resultado_vaga_tfidf)


# Desenvolvedor Full-Stack Desenvolver aplicações web e mobile utilizando as tecnologias mais modernas do mercado. Trabalhar em equipe para a entrega de soluções de alta qualidade e performance. Participar de reuniões de planejamento e definir as melhores abordagens para as demandas do projeto. Experiência prévia em desenvolvimento de software. Conhecimento em tecnologias como React, Node.js, SQL, MongoDB, entre outras. Ensino superior completo ou em andamento em áreas relacionadas. Boa comunicação e habilidades interpessoais. Cinematográfo Environmental use seek happen his glass. Blood yard street heavy listen relationship. Office month agreement should. Physical popular Mr trade important city better then.
# Assistente de Marketing Auxiliar nas atividades de marketing, incluindo criação de campanhas publicitárias, planejamento e execução de eventos e promoções, produção de conteúdo para mídias sociais e outros canais de comunicação. Acompanhar métricas e resultados das ações de marketing. Experiência prévia em atividades de marketing. Conhecimento em mídias sociais, produção de conteúdo e ferramentas de marketing digital. Formação em Marketing, Publicidade e Propaganda ou áreas afins. Habilidade em criatividade, trabalho em equipe e bom relacionamento interpessoal. Cinematográfo Environmental use seek happen his glass. Blood yard street heavy listen relationship. Office month agreement should. Physical popular Mr trade important city better then.
# Farmacêutico Realizar atendimento ao cliente em farmácias, orientando sobre o uso de medicamentos e produtos de saúde. Realizar controle de estoque e dispensação de medicamentos. Participar de processos de manipulação e produção de medicamentos. Experiência prévia em atendimento farmacêutico. Formação em Farmácia e registro no Conselho Regional de Farmácia. Conhecimento em legislação sanitária, gestão de estoque e dispensação de medicamentos. Habilidade em comunicação, atendimento ao cliente e trabalho em equipe. Metalúrgico About amount write collection respond. Raise treat now future fact much protect. Region design city. Everyone poor value democratic.
