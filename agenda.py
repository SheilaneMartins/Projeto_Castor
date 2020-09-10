class Compromisso:
    """
    Classe para o objeto Compromisso.
    """

    def __init__(self, desc: str, data='', hora='', pri='', contexto='', proj=''):
        self.data = data
        self.hora = hora
        self.pri = pri
        self.desc = desc
        self.contexto = contexto
        self.proj = proj

RED = "\033[1;31m"
BLUE = "\033[1;34m"
CYAN = "\033[1;36m"
GREEN = "\033[0;32m"
RESET = "\033[0;0m"
BOLD = "\033[;1m"
REVERSE = "\033[;7m"
YELLOW = "\033[0;33m"

ADICIONAR = 'a'
REMOVER = 'r'
FAZER = 'f'
PRIORIZAR = 'p'
LISTAR = 'l'


def soDigitos(valor: str):
    """
    Verifica se todos os caracteres são numéricos.

    :param valor:
    :return: Bool
    """
    return type(int(valor)) == int


def horaValida(hhmm: str):
    """
    Validação do parâmetro relativo ao horário

    :param hhmm:
    :return: Bool
    """
    if len(hhmm) == 4 and soDigitos(hhmm):
        h, m = int(hhmm[:2]), int(hhmm[2:])
        if (h not in range(0, 24)) or (m not in range(0, 60)):
            return False
        return True
    else:
        return False


def anoBissexto(aaaa: str):
    """
    Verifica se o ano é bissexto, onde Fevereiro tem 29 dias.

    :param aaaa:
    :return: Bool
    """
    return int(aaaa) % 4 == 0


MESES = {
    '31_DIAS': ['01', '03', '05', '07', '08', '10', '12'],
    '30_DIAS': ['04', '06', '09', '11'],
    'FEVEREIRO': ['02']
}


def dataValida(ddMMaaaa: str):
    """
    Valida o campo data.

    :param ddMMaaaa:
    :return: Bool
    """
    if len(ddMMaaaa) == 8 and soDigitos(ddMMaaaa):
        dd = ddMMaaaa[0:2]
        MM = ddMMaaaa[2:4]
        aaaa = ddMMaaaa[4:]
        # verificacao inicial
        if int(dd) in range(1, 32) and (int(MM) in range(1, 13)) and (len(aaaa) == 4):
            _ = int(dd)
            if _ >= 29:
                # Fevereiro apenas em ano bissexto
                if MM in MESES['FEVEREIRO']:
                    # Fevereiro nunca passa de 29 dias
                    if _ > 29:
                        return False
                    # permitido caso o ano seja bissexto
                    if anoBissexto(aaaa) == False:
                        return False
                # dia 31 em meses com 30 dias ou Fevereiro
                if _ == 31 and MM not in MESES['31_DIAS']:
                    return False
            return True
    else:
        return False


def projetoValido(projeto: str):
    """
    Valida o campo projeto.

    :param projeto:
    :return: Bool
    """
    return len(projeto) >= 2 and projeto.startswith('+')


def contextoValido(contexto: str):
    """
    Valida o campo contexto.

    :param contexto:
    :return: Bool
    """
    return len(contexto) >= 2 and contexto.startswith('@')


ALFABETO_MAIUSC = [letra for letra in 'ABCDEFGHIJKLMNOPQRSTUVXWYZ']


def prioridadeValida(prioridade: str):
    """
    Valida o campo prioridade.

    :param contexto:
    :return: Bool
    """
    return len(prioridade) == 3 and prioridade.startswith('(') and prioridade.endswith(')') and prioridade
    [1] in ALFABETO_MAIUSC


import re


def organizar(compromissos: [str]):
    """
    Cria lista de objetos do tipo Compromisso

    :param compromissos: list(str)
    :return: lista de objetos do tipo Compromisso
    """
    lista = []
    for compromisso in compromissos:
        data, hora, pri, desc, contexto, proj = '', '', '', '', '', ''
        try:
            data = re.findall(pattern='(\d{8})\s+', string=compromisso)[0]
            compromisso = re.sub(pattern='(\d{8})\s+', repl='', string=compromisso)
        except:
            pass
        try:
            hora = re.findall(pattern='\W*(\d{4})\s+', string=compromisso)[0]
            compromisso = re.sub(pattern='\W*(\d{4})\s+', repl='', string=compromisso)
        except:
            pass
        try:
            pri = re.findall(pattern='(\(\w\))', string=compromisso)[0]
            compromisso = re.sub(pattern='(\(\w\))', repl='', string=compromisso)
        except:
            pass
        try:
            contexto = re.findall(pattern='(\@[\w\d]*)', string=compromisso)[0]
            compromisso = re.sub(pattern='(\@[\w\d]*)', repl='', string=compromisso)
        except:
            pass
        try:
            proj = re.findall(pattern='(\+[\w\d]*)', string=compromisso)[0]
            compromisso = re.sub(pattern='(\+[\w\d]*)', repl='', string=compromisso)
        except:
            pass
        desc = compromisso.strip()
        c = Compromisso(desc=desc, data=data, hora=hora, pri=pri, contexto=contexto, proj=proj)
        lista.append(c)
    return lista


def adicionar(descricao: str, extras: tuple):
    """
    Adiciona um compromisso a agenda.
    """
    if type(extras) == str:
        extras = [extras]
    extras = ' '.join([e for e in extras])
    compromisso = descricao + ' ' + extras
    with open(file='todo.txt', mode='a') as f:
        data, hora, pri, desc, contexto, proj = '', '', '', '', '', ''
        try:
            data = re.findall(pattern='(\d{8})\s+', string=compromisso)[0]
            compromisso = re.sub(pattern='(\d{8})\s+', repl='', string=compromisso)
            if dataValida(data):
                data = data
            else:
                data = ''
        except:
            pass
        try:
            hora = re.findall(pattern='\W*(\d{4})\s+', string=compromisso)[0]
            compromisso = re.sub(pattern='\W*(\d{4})\s+', repl='', string=compromisso)
            if horaValida(hora):
                hora = hora
            else:
                hora = ''
        except:
            pass
        try:
            pri = re.findall(pattern='(\(\w\))', string=compromisso)[0]
            compromisso = re.sub(pattern='(\(\w\))', repl='', string=compromisso)
        except:
            pass
        try:
            contexto = re.findall(pattern='(\@[\w\d]*)', string=compromisso)[0]
            compromisso = re.sub(pattern='(\@[\w\d]*)', repl='', string=compromisso)
            if contextoValido(contexto):
                contexto = contexto
            else:
                contexto = ''
        except:
            pass
        try:
            proj = re.findall(pattern='(\+[\w\d]*)', string=compromisso)[0]
            compromisso = re.sub(pattern='(\+[\w\d]*)', repl='', string=compromisso)
            if projetoValido(proj):
                proj = proj
            else:
                proj = ''
        except:
            pass
        desc = compromisso.strip()
        compromisso = ' '.join([data, hora, pri, desc, contexto, proj]).replace('  ', '') + '\n'
        f.write(compromisso.lstrip())


def ordenarPorData(lista_comp: [Compromisso]):
    """
    :param lista_comp:
    :return: lista de objetos ordenada pela data
    """
    for c in lista_comp:
        if c.data == '':
            c.data = '99999999'
    lista_comp.sort(key=lambda a: a.data)
    for c in lista_comp:
        if c.data == '99999999':
            c.data = ''
    return lista_comp


def ordenarPorHora(lista_comp: [Compromisso]):
    """
    :param lista_comp:
    :return: Lista de Objetos ordenada pela Hora
    """
    for c in lista_comp:
        if c.hora == '':
            c.hora = '9999'
    lista_comp.sort(key=lambda a: a.hora)
    for c in lista_comp:
        if c.hora == '9999':
            c.hora = ''
    return lista_comp


def ordenarPorPri(lista_comp: [Compromisso]):
    """
    :param lista_comp:
    :return: Lista de Objetos ordenada pela prioridade
    """
    for c in lista_comp:
        if c.pri == '':
            c.pri = '(X)'
    lista_comp.sort(key=lambda a: a.pri)
    for c in lista_comp:
        if c.pri == '(X)':
            c.pri = ''
    return lista_comp


def listar(arquivo='todo.txt'):
    with open(file=arquivo, mode='r') as f:
        lines = f.readlines()
    org = organizar(compromissos=lines)
    org = ordenarPorPri(org)
    for c in org:
        print(c.data, c.hora, c.pri, c.desc, c.contexto, c.proj)
    return org


def remover(index: int):
    _ = None
    with open(file='todo.txt', mode='r') as f:
        _ = f.readlines()
    if index not in range(len(_) + 1):
        print("Índice da atividade não existe")
    else:
        try:
            print(f'Compromisso: {_[index]}')
            del _[index]
            with open(file='todo.txt', mode='w') as f:
                for c in _:
                    f.write(c)
        except IndexError:
            print("Índice da atividade não existe")
    with open(file='todo.txt', mode='r') as f:
        _ = f.readlines()


def priorizar(index: int, p: str):
    with open(file='todo.txt', mode='r') as f:
        lines = f.readlines()
        print('Total de compromissos:', len(lines))
    if index not in range(len(lines) + 1):
        print("Índice da atividade não existe")
    else:
        try:
            c_n = organizar([lines[index - 1]])[0]
            c_n.pri = f'({p.upper()})'
            lines[index - 1] = ' '.join([c_n.data, c_n.hora, c_n.pri, c_n.desc, c_n.contexto, c_n.proj])
            lines[index - 1] = lines[index - 1].replace('  ', ' ').replace('\n', '').rstrip().lstrip()
            lines = [l.replace('\n', '') for l in lines]
            print('>>>', lines[index - 1])
            with open(file='todo.txt', mode='wt') as f:
                for line in lines:
                    print('LINE:', line)
                    # Está escrevendo de forma concatenada
                    f.write(line)
        except IndexError:
            print("Índice da atividade não existe")


def fazer(index: int):
    with open(file='todo.txt', mode='r') as f:
        _ = f.readlines()
    if index not in range(len(_) + 1):
        print("Índice da atividade não existe")
    else:
        try:
            print(f'Compromisso: {_[index]}')
            with open(file='done.txt', mode='a') as f:
                f.write(_[index])
            del _[index]
            with open(file='todo.txt', mode='w') as f:
                for c in _:
                    f.write(c)
        except IndexError:
            print("Índice da atividade não existe")


def processarComandos(comandos):
    if comandos[1] == ADICIONAR:
        comandos.pop(0)  # remove 'agenda.py'
        comandos.pop(0)  # remove 'adicionar'
        itemParaAdicionar = organizar([' '.join(comandos)])[0]
        # itemParaAdicionar = (descricao, (prioridade, data, hora, contexto, projeto))
        adicionar(itemParaAdicionar[0], itemParaAdicionar[1])  # novos itens não têm prioridade
    elif comandos[1] == LISTAR:
        return
        ################ COMPLETAR

    elif comandos[1] == REMOVER:
        return

        ################ COMPLETAR

    elif comandos[1] == FAZER:
        return

        ################ COMPLETAR

    elif comandos[1] == PRIORIZAR:
        return

        ################ COMPLETAR

    else:
        print("Comando inválido.")
