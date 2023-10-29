from datetime import datetime

def calcular_idade(data_nascimento: str) -> int:

    """ Retorna a idade baseado na data de nascimento fornecida.
 
    Parameters
    ------------
        data_nascimento: str
            A data de nascimento que deve ser no formato yyyy-mm-dd
    Return
    -----------
        idade : int
            A idade calculada. 
    """

    data_nascimento = datetime.strptime(data_nascimento, '%Y-%m-%d')
    data_atual = datetime.now()
    diferenca = data_atual - data_nascimento
    idade = diferenca.days // 365

    return idade

print(calcular_idade('2006-10-13'))
