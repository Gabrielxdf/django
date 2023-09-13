#!/bin/bash
#SBERT
python3 process_vaga_2.py "paraphrase-multilingual-MiniLM-L12-v2" "mean";
python3 process_candidato_2.py "paraphrase-multilingual-MiniLM-L12-v2" "mean";
echo -e "\n RESULTADOS PARA SBERT - MEAN" | tee -a resultados.txt
python3 analise_recomendacao_4.py | tee -a resultados.txt;

python3 process_vaga_2.py "paraphrase-multilingual-MiniLM-L12-v2" "mean_sqrt";
python3 process_candidato_2.py "paraphrase-multilingual-MiniLM-L12-v2" "mean_sqrt";
echo -e "\n RESULTADOS PARA SBERT - MEAN_SQRT" | tee -a resultados.txt
python3 analise_recomendacao_4.py | tee -a resultados.txt;

python3 process_vaga_2.py "paraphrase-multilingual-MiniLM-L12-v2" "cls";
python3 process_candidato_2.py "paraphrase-multilingual-MiniLM-L12-v2" "cls";
echo -e "\n RESULTADOS PARA SBERT - CLS" | tee -a resultados.txt
python3 analise_recomendacao_4.py | tee -a resultados.txt;

python3 process_vaga_2.py "paraphrase-multilingual-MiniLM-L12-v2" "max";
python3 process_candidato_2.py "paraphrase-multilingual-MiniLM-L12-v2" "max";
echo -e "\n RESULTADOS PARA SBERT - MAX" | tee -a resultados.txt
python3 analise_recomendacao_4.py | tee -a resultados.txt;

#BERTIMBAU-BASE
python3 process_vaga_2.py "neuralmind/bert-base-portuguese-cased" "mean";
python3 process_candidato_2.py "neuralmind/bert-base-portuguese-cased" "mean";
echo -e "\n RESULTADOS PARA BERTIMBAU-BASE - MEAN" | tee -a resultados.txt
python3 analise_recomendacao_4.py | tee -a resultados.txt;

python3 process_vaga_2.py "neuralmind/bert-base-portuguese-cased" "mean_sqrt";
python3 process_candidato_2.py "neuralmind/bert-base-portuguese-cased" "mean_sqrt";
echo -e "\n RESULTADOS PARA BERTIMBAU-BASE - MEAN_SQRT" | tee -a resultados.txt
python3 analise_recomendacao_4.py | tee -a resultados.txt;

python3 process_vaga_2.py "neuralmind/bert-base-portuguese-cased" "cls";
python3 process_candidato_2.py "neuralmind/bert-base-portuguese-cased" "cls";
echo -e "\n RESULTADOS PARA BERTIMBAU-BASE - CLS" | tee -a resultados.txt
python3 analise_recomendacao_4.py | tee -a resultados.txt;

python3 process_vaga_2.py "neuralmind/bert-base-portuguese-cased" "max";
python3 process_candidato_2.py "neuralmind/bert-base-portuguese-cased" "max";
echo -e "\n RESULTADOS PARA BERTIMBAU-BASE - MAX" | tee -a resultados.txt
python3 analise_recomendacao_4.py | tee -a resultados.txt;

#BERTIMBAU-LARGE
python3 process_vaga_2.py "neuralmind/bert-large-portuguese-cased" "mean";
python3 process_candidato_2.py "neuralmind/bert-large-portuguese-cased" "mean";
echo -e "\n RESULTADOS PARA BERTIMBAU-LARGE - MEAN" | tee -a resultados.txt
python3 analise_recomendacao_4.py | tee -a resultados.txt;

python3 process_vaga_2.py "neuralmind/bert-large-portuguese-cased" "mean_sqrt";
python3 process_candidato_2.py "neuralmind/bert-large-portuguese-cased" "mean_sqrt";
echo -e "\n RESULTADOS PARA BERTIMBAU-LARGE - MEAN_SQRT" | tee -a resultados.txt
python3 analise_recomendacao_4.py | tee -a resultados.txt;

python3 process_vaga_2.py "neuralmind/bert-large-portuguese-cased" "cls";
python3 process_candidato_2.py "neuralmind/bert-large-portuguese-cased" "cls";
echo -e "\n RESULTADOS PARA BERTIMBAU-LARGE - CLS" | tee -a resultados.txt
python3 analise_recomendacao_4.py | tee -a resultados.txt;

python3 process_vaga_2.py "neuralmind/bert-large-portuguese-cased" "max";
python3 process_candidato_2.py "neuralmind/bert-large-portuguese-cased" "max";
echo -e "\n RESULTADOS PARA BERTIMBAU-LARGE - MAX" | tee -a resultados.txt
python3 analise_recomendacao_4.py | tee -a resultados.txt;

#PTT5-BASE
python3 process_vaga_2.py "unicamp-dl/ptt5-base-portuguese-vocab" "mean";
python3 process_candidato_2.py "unicamp-dl/ptt5-base-portuguese-vocab" "mean";
echo -e "\n RESULTADOS PARA PTT5-BASE - MEAN" | tee -a resultados.txt
python3 analise_recomendacao_4.py | tee -a resultados.txt;

python3 process_vaga_2.py "unicamp-dl/ptt5-base-portuguese-vocab" "mean_sqrt";
python3 process_candidato_2.py "unicamp-dl/ptt5-base-portuguese-vocab" "mean_sqrt";
echo -e "\n RESULTADOS PARA PTT5-BASE - MEAN_SQRT" | tee -a resultados.txt
python3 analise_recomendacao_4.py | tee -a resultados.txt;

python3 process_vaga_2.py "unicamp-dl/ptt5-base-portuguese-vocab" "cls";
python3 process_candidato_2.py "unicamp-dl/ptt5-base-portuguese-vocab" "cls";
echo -e "\n RESULTADOS PARA PTT5-BASE - CLS" | tee -a resultados.txt
python3 analise_recomendacao_4.py | tee -a resultados.txt;

python3 process_vaga_2.py "unicamp-dl/ptt5-base-portuguese-vocab" "max";
python3 process_candidato_2.py "unicamp-dl/ptt5-base-portuguese-vocab" "max";
echo -e "\n RESULTADOS PARA PTT5-BASE - MAX" | tee -a resultados.txt
python3 analise_recomendacao_4.py | tee -a resultados.txt;

#PTT5-LARGE
python3 process_vaga_2.py "unicamp-dl/ptt5-large-portuguese-vocab" "mean";
python3 process_candidato_2.py "unicamp-dl/ptt5-large-portuguese-vocab" "mean";
echo -e "\n RESULTADOS PARA PTT5-LARGE - MEAN" | tee -a resultados.txt
python3 analise_recomendacao_4.py | tee -a resultados.txt;

python3 process_vaga_2.py "unicamp-dl/ptt5-large-portuguese-vocab" "mean_sqrt";
python3 process_candidato_2.py "unicamp-dl/ptt5-large-portuguese-vocab" "mean_sqrt";
echo -e "\n RESULTADOS PARA PTT5-LARGE - MEAN_SQRT" | tee -a resultados.txt
python3 analise_recomendacao_4.py | tee -a resultados.txt;

python3 process_vaga_2.py "unicamp-dl/ptt5-large-portuguese-vocab" "cls";
python3 process_candidato_2.py "unicamp-dl/ptt5-large-portuguese-vocab" "cls";
echo -e "\n RESULTADOS PARA PTT5-LARGE - CLS" | tee -a resultados.txt
python3 analise_recomendacao_4.py | tee -a resultados.txt;

python3 process_vaga_2.py "unicamp-dl/ptt5-large-portuguese-vocab" "max";
python3 process_candidato_2.py "unicamp-dl/ptt5-large-portuguese-vocab" "max";
echo -e "\n RESULTADOS PARA PTT5-LARGE - MAX" | tee -a resultados.txt
python3 analise_recomendacao_4.py | tee -a resultados.txt;

#XLM-R BASE
python3 process_vaga_2.py "xlm-roberta-base" "mean";
python3 process_candidato_2.py "xlm-roberta-base" "mean";
echo -e "\n RESULTADOS PARA XML-R BASE - MEAN" | tee -a resultados.txt
python3 analise_recomendacao_4.py | tee -a resultados.txt;

python3 process_vaga_2.py "xlm-roberta-base" "mean_sqrt";
python3 process_candidato_2.py "xlm-roberta-base" "mean_sqrt";
echo -e "\n RESULTADOS PARA XML-R BASE - MEAN_SQRT" | tee -a resultados.txt
python3 analise_recomendacao_4.py | tee -a resultados.txt;

python3 process_vaga_2.py "xlm-roberta-base" "cls";
python3 process_candidato_2.py "xlm-roberta-base" "cls";
echo -e "\n RESULTADOS PARA XML-R BASE - CLS" | tee -a resultados.txt
python3 analise_recomendacao_4.py | tee -a resultados.txt;

python3 process_vaga_2.py "xlm-roberta-base" "max";
python3 process_candidato_2.py "xlm-roberta-base" "max";
echo -e "\n RESULTADOS PARA XML-R BASE - MAX" | tee -a resultados.txt
python3 analise_recomendacao_4.py | tee -a resultados.txt;

#XLM-R LARGE
python3 process_vaga_2.py "xlm-roberta-large" "mean";
python3 process_candidato_2.py "xlm-roberta-large" "mean";
echo -e "\n RESULTADOS PARA XML-R LARGE - MEAN" | tee -a resultados.txt
python3 analise_recomendacao_4.py | tee -a resultados.txt;

python3 process_vaga_2.py "xlm-roberta-large" "mean_sqrt";
python3 process_candidato_2.py "xlm-roberta-large" "mean_sqrt";
echo -e "\n RESULTADOS PARA XML-R LARGE - MEAN_SQRT" | tee -a resultados.txt
python3 analise_recomendacao_4.py | tee -a resultados.txt;

python3 process_vaga_2.py "xlm-roberta-large" "cls";
python3 process_candidato_2.py "xlm-roberta-large" "cls";
echo -e "\n RESULTADOS PARA XML-R LARGE - CLS" | tee -a resultados.txt
python3 analise_recomendacao_4.py | tee -a resultados.txt;

python3 process_vaga_2.py "xlm-roberta-large" "max";
python3 process_candidato_2.py "xlm-roberta-large" "max";
echo -e "\n RESULTADOS PARA XML-R LARGE - MAX" | tee -a resultados.txt
python3 analise_recomendacao_4.py | tee -a resultados.txt;
