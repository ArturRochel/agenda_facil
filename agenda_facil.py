from dataclasses import dataclass
from datetime import datetime

HORARIO_INICIO = 8
HORARIO_FIM = 17

class ErroMarcacao(Exception):
    """Erro ao marcar consulta"""

@dataclass
class Atendimento:
    paciente: str
    profissional: str
    data: str
    hora: int
    duracao: int
    status: str = "MARCADO"

agenda: list[Atendimento] = []

def _validar_data(data_str) -> bool:
    """Validar se a data inserida no sistema é uma data válida.

    Está função recebe uma data como string no formato AAAA-MM-DD e retorna se é uma
    data válida ou não.

    Args:
        data_str (str): A data inserida pelo usuário no sistema.

    Returns:
        bool: True se a data for válida e False caso não seja uma data válida.
    """
    try:
        datetime.strptime(data_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def _imprimir_mensagem(mensagem: str) -> None:
    """Imprime no terminal a mensagem recebida.

    Essa função possui a responsabilidade de exibir as mensagens, printar no terminal.

    Args:
        mensagem (str): A mensagem que deve ser exibida.

    Retunr:
        None: Apenas a ação é execultada, sem retorno de nada pela função.
    """
    print(mensagem)

def _buscar_consulta(paciente, data, hora) -> Atendimento|None:
    """Função que busca uma consulta no sistema.

    Esta função interna possui a responsabilidade de buscar uma consulta nos agendamentos.

    Args:
        paciente (str): Nome do paciente.
        data (str): Data na qual a consulta está marcada, no formato AAAA-MM-DD e como string.
        hora (int): Hora na qual a consulta está agendada.

    Returns:
        Atendimento: Retorna o objeto do atendimento, caso a consulta seja encontrada.
        None: Retorna None caso a consulta não seja encontrada.
    """ 
    for consulta in agenda:
        if paciente == consulta.paciente and data == consulta.data and hora == consulta.hora:
            return consulta

    

def _verificar_disponibilidade(profissional, data, hora) -> bool:
    """Verifica se um profissional está disponível em determinada data e horário.

    Essa função possui a responsabilidade de verificar a disponibilidade de um profissional,
    em determina data e hora.

    Args:
        profissional (str): Nome do profissional que deseja ver a disponibilidade.
        data (str): Data no formato AAAA-MM-AA que deseja ver a disponibilidade.
        hora (int): Horário no qual deseja ver a disponibilidade.

    Returns:
        bool: Retorna True se a agenda estiver vaga e False caso não esteja.
    """
    for consulta in agenda:
        if consulta.profissional == profissional and consulta.data == data and consulta.hora == hora:
            return False

    return True

def marcar_consulta(paciente, profissional, data, hora, duracao):
    """Realiza a marcação de uma consulta.

    Essa função possui a responsabilidade de marcar uma consulta para um paciente em determinado
    horário, data e com profissional, caso esteja disponível.

    Args:
        paciente (str): Nome do paciente.
        profissional (str): Nome do profissional para o qual o paciente deseja marcar.
        data (str): Data da consulta desejada.
        hora (int): Horário da consulta desejada.
        duracao (int): Duração do horário da consulta.

    Returns:
        str: 
    """
    if duracao > 0 and HORARIO_INICIO <= hora <= HORARIO_FIM and _validar_data(data):
        if duracao > 60 and hora == 17:
            return _imprimir_mensagem("A consulta ultrapassa o horário de funcionamento da clínica")
        if not _verificar_disponibilidade(profissional, data, hora):
            return _imprimir_mensagem("Horário ocupado")
    else:
        return _imprimir_mensagem("Erro ao marcar consulta, duração, horário ou data estão incorretos")
        
    try:
        agenda.append(Atendimento(paciente, profissional, data, hora, duracao, "MARCADO"))
    except:
        raise ErroMarcacao("Erro interno ao marcar consulta")

    return _imprimir_mensagem(f"Atendimento marcado para {paciente}")
       
def remarcar_consulta(paciente, data, hora, nova_data, nova_hora):
    if not _validar_data(data) and _validar_data(nova_data) and HORARIO_INICIO <= hora <= HORARIO_FIM and HORARIO_INICIO <= nova_hora <= HORARIO_FIM:
        return _imprimir_mensagem("Erro ao marcar consulta, duração, horário ou data estão incorretos")
    
    consulta_atual = _buscar_consulta(paciente, data, hora)

    if consulta_atual.duracao > 60 and nova_hora == 17:
        return _imprimir_mensagem("A consulta ultrapassa o horário de funcionamento da clínica")

    if _verificar_disponibilidade(consulta_atual.profissional, nova_data, nova_hora):
        consulta_atual.data = nova_data
        consulta_atual.hora = nova_hora
    else:
        _imprimir_mensagem("Horário ocupado")

    return _imprimir_mensagem("Remarcado")

def listar_atendimentos_do_dia(data):
    if not _validar_data(data):
       return _imprimir_mensagem("Data inválida") 

    for atendimento in agenda:
        if atendimento.data == data:
            _imprimir_mensagem(f"{atendimento.hora} {atendimento.paciente} {atendimento.profissional} {atendimento.status}")


# marcar_consulta(PACIENTE, PROFISSIONAL, DATA, HORA, DURAÇÃO)
marcar_consulta("Ana", "Dra. Silva", "2026-10-05", 9, 30)
marcar_consulta("Bruno", "Dra. Silva", "2026-10-05", 9, 30)
marcar_consulta("Carla", "Dra. Souza", "2026-10-05", 14, 60)
remarcar_consulta("Ana", "2026-10-05", 9, "2026-10-06", 10)
listar_atendimentos_do_dia("2026-10-05")