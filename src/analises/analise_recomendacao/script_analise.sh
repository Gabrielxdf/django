#!/bin/bash
#PTT5-BASE
python3 process_vaga.py "unicamp-dl/ptt5-base-portuguese-vocab" "mean";
python3 process_candidato.py "unicamp-dl/ptt5-base-portuguese-vocab" "mean";
echo -e "\n RESULTADOS PARA PTT5-BASE - MEAN" | tee -a resultados.txt
python3 analise_recomendacao_3.py | tee -a resultados.txt;

python3 process_vaga.py "unicamp-dl/ptt5-base-portuguese-vocab" "mean_sqrt";
python3 process_candidato.py "unicamp-dl/ptt5-base-portuguese-vocab" "mean_sqrt";
echo -e "\n RESULTADOS PARA PTT5-BASE - MEAN_SQRT" | tee -a resultados.txt
python3 analise_recomendacao_3.py | tee -a resultados.txt;

python3 process_vaga.py "unicamp-dl/ptt5-base-portuguese-vocab" "cls";
python3 process_candidato.py "unicamp-dl/ptt5-base-portuguese-vocab" "cls";
echo -e "\n RESULTADOS PARA PTT5-BASE - CLS" | tee -a resultados.txt
python3 analise_recomendacao_3.py | tee -a resultados.txt;

python3 process_vaga.py "unicamp-dl/ptt5-base-portuguese-vocab" "max";
python3 process_candidato.py "unicamp-dl/ptt5-base-portuguese-vocab" "max";
echo -e "\n RESULTADOS PARA PTT5-BASE - MAX" | tee -a resultados.txt
python3 analise_recomendacao_3.py | tee -a resultados.txt;

#PTT5-LARGE
python3 process_vaga.py "unicamp-dl/ptt5-large-portuguese-vocab" "mean";
python3 process_candidato.py "unicamp-dl/ptt5-large-portuguese-vocab" "mean";
echo -e "\n RESULTADOS PARA PTT5-LARGE - MEAN" | tee -a resultados.txt
python3 analise_recomendacao_3.py | tee -a resultados.txt;

python3 process_vaga.py "unicamp-dl/ptt5-large-portuguese-vocab" "mean_sqrt";
python3 process_candidato.py "unicamp-dl/ptt5-large-portuguese-vocab" "mean_sqrt";
echo -e "\n RESULTADOS PARA PTT5-LARGE - MEAN_SQRT" | tee -a resultados.txt
python3 analise_recomendacao_3.py | tee -a resultados.txt;

python3 process_vaga.py "unicamp-dl/ptt5-large-portuguese-vocab" "cls";
python3 process_candidato.py "unicamp-dl/ptt5-large-portuguese-vocab" "cls";
echo -e "\n RESULTADOS PARA PTT5-LARGE - CLS" | tee -a resultados.txt
python3 analise_recomendacao_3.py | tee -a resultados.txt;

python3 process_vaga.py "unicamp-dl/ptt5-large-portuguese-vocab" "max";
python3 process_candidato.py "unicamp-dl/ptt5-large-portuguese-vocab" "max";
echo -e "\n RESULTADOS PARA PTT5-LARGE - MAX" | tee -a resultados.txt
python3 analise_recomendacao_3.py | tee -a resultados.txt;

#XLM-R BASE
python3 process_vaga.py "xlm-roberta-base" "mean";
python3 process_candidato.py "xlm-roberta-base" "mean";
echo -e "\n RESULTADOS PARA XML-R BASE - MEAN" | tee -a resultados.txt
python3 analise_recomendacao_3.py | tee -a resultados.txt;

python3 process_vaga.py "xlm-roberta-base" "mean_sqrt";
python3 process_candidato.py "xlm-roberta-base" "mean_sqrt";
echo -e "\n RESULTADOS PARA XML-R BASE - MEAN_SQRT" | tee -a resultados.txt
python3 analise_recomendacao_3.py | tee -a resultados.txt;

python3 process_vaga.py "xlm-roberta-base" "cls";
python3 process_candidato.py "xlm-roberta-base" "cls";
echo -e "\n RESULTADOS PARA XML-R BASE - CLS" | tee -a resultados.txt
python3 analise_recomendacao_3.py | tee -a resultados.txt;

python3 process_vaga.py "xlm-roberta-base" "max";
python3 process_candidato.py "xlm-roberta-base" "max";
echo -e "\n RESULTADOS PARA XML-R BASE - MAX" | tee -a resultados.txt
python3 analise_recomendacao_3.py | tee -a resultados.txt;

#XLM-R LARGE
python3 process_vaga.py "xlm-roberta-large" "mean";
python3 process_candidato.py "xlm-roberta-large" "mean";
echo -e "\n RESULTADOS PARA XML-R LARGE - MEAN" | tee -a resultados.txt
python3 analise_recomendacao_3.py | tee -a resultados.txt;

python3 process_vaga.py "xlm-roberta-large" "mean_sqrt";
python3 process_candidato.py "xlm-roberta-large" "mean_sqrt";
echo -e "\n RESULTADOS PARA XML-R LARGE - MEAN_SQRT" | tee -a resultados.txt
python3 analise_recomendacao_3.py | tee -a resultados.txt;

python3 process_vaga.py "xlm-roberta-large" "cls";
python3 process_candidato.py "xlm-roberta-large" "cls";
echo -e "\n RESULTADOS PARA XML-R LARGE - CLS" | tee -a resultados.txt
python3 analise_recomendacao_3.py | tee -a resultados.txt;

python3 process_vaga.py "xlm-roberta-large" "max";
python3 process_candidato.py "xlm-roberta-large" "max";
echo -e "\n RESULTADOS PARA XML-R LARGE - MAX" | tee -a resultados.txt
python3 analise_recomendacao_3.py | tee -a resultados.txt;
