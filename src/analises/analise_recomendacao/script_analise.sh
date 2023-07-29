#!/bin/bash
python3 process_vaga.py "unicamp-dl/ptt5-base-portuguese-vocab";
python3 process_candidato.py "unicamp-dl/ptt5-base-portuguese-vocab";
echo RESULTADOS PARA PTT5-BASE | tee -a resultados.txt
python3 analise_recomendacao_3.py | tee -a resultados.txt;

python3 process_vaga.py "unicamp-dl/ptt5-large-portuguese-vocab";
python3 process_candidato.py "unicamp-dl/ptt5-large-portuguese-vocab";
echo RESULTADOS PARA PTT5-LARGE | tee -a resultados.txt
python3 analise_recomendacao_3.py | tee -a resultados.txt;

python3 process_vaga.py "xlm-roberta-base";
python3 process_candidato.py "xlm-roberta-base";
echo RESULTADOS PARA XML-R BASE | tee -a resultados.txt
python3 analise_recomendacao_3.py | tee -a resultados.txt;

python3 process_vaga.py "xlm-roberta-large";
python3 process_candidato.py "xlm-roberta-large";
echo RESULTADOS PARA XML-R LARGE | tee -a resultados.txt
python3 analise_recomendacao_3.py | tee -a resultados.txt;
