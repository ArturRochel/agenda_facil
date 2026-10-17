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
    try:
        datetime.strptime(data_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def _imprimir_mensagem(mensagem: str) -> str:
    print(mensagem)

def _buscar_consulta(paciente, data, hora) -> Atendimento:
    try:
        for consulta in agenda:
            if paciente == consulta.paciente and data == consulta.data and hora == consulta.hora:
                return consulta
    except:
        raise ValueError("A consulta não foi encontrada no sistema")

def _verificar_disponibilidade(profissional, data, hora) -> bool:
    for consulta in agenda:
        if consulta.profissional == profissional and consulta.data == data and consulta.hora == hora:
            return False

    return True

def marcar_consulta(paciente, profissional, data, hora, duracao):
    if duracao > 0 and HORARIO_INICIO <= hora <= HORARIO_FIM and _validar_data(data):
        if duracao > 60 and hora == 17:
            return _imprimir_mensagem("A consulta ultrapassa o horário de funcionamento da clínica")
        if _verificar_disponibilidade(profissional, data, hora):
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
            _imprimir_mensagem(f"{atendimento.hora}, {atendimento.paciente}, {atendimento.profissional}, {atendimento.status}")


marcar_consulta("Ana", "Dr. Silva", "2026-10-05", 9, 30)
marcar_consulta("Bruno", "Dr. Silva", "2026-10-05", 9, 30)
marcar_consulta("Carla", "Dra. Souza", "2026-10-05", 14, 60)
remarcar_consulta("Ana", "2026-10-05", 9, "2026-10-06", 10)
listar_atendimentos_do_dia("2026-10-05")