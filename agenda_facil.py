"""Módulo de agendamento de consultas médicas.

Este módulo fornece funções para marcação, remarcação e listagem de consultas,
assegurando a validação de horários de funcionamento, duração e prevenção de
sobreposição de horários entre profissionais e pacientes.
"""

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Optional

HORARIO_INICIO = 8
HORARIO_FIM = 17


class ErroAgenda(Exception):
    """Exceção base para erros relacionados às regras da agenda."""


class HorarioInvalidoError(ValueError, ErroAgenda):
    """Exceção levantada quando um horário ou data é inválido ou fora do expediente."""


class ConsultaNaoEncontradaError(ErroAgenda):
    """Exceção levantada quando uma consulta buscada não existe na agenda."""


@dataclass
class Atendimento:
    """Representa um atendimento médico agendado.

    Attributes:
        paciente: Nome do paciente.
        profissional: Nome do profissional de saúde.
        data: Data da consulta no formato AAAA-MM-DD.
        hora: Hora inteira de início do atendimento (0 a 23).
        duracao: Duração do atendimento em minutos.
        status: Estado atual do agendamento (padrão 'MARCADO').
    """

    paciente: str
    profissional: str
    data: str
    hora: int
    duracao: int
    status: str = "MARCADO"

    @property
    def inicio(self) -> datetime:
        """Calcula o datetime exato do início da consulta."""
        return datetime.strptime(f"{self.data} {self.hora:02d}:00", "%Y-%m-%d %H:%M")

    @property
    def fim(self) -> datetime:
        """Calcula o datetime exato de término da consulta."""
        return self.inicio + timedelta(minutes=self.duracao)


agenda: list[Atendimento] = []


def _validar_data(data_str: str) -> bool:
    """Valida se uma data em formato texto é uma data válida do calendário.

    Args:
        data_str (str): Data a ser validada no formato AAAA-MM-DD.

    Returns:
        bool: True se a data for válida, False caso contrário.
    """
    try:
        datetime.strptime(data_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def _imprimir_mensagem(mensagem: str) -> None:
    """Imprime uma mensagem no terminal.

    Args:
        mensagem (str): Mensagem a ser exibida.

    Returns:
        None
    """
    print(mensagem)


def _dentro_do_expediente(inicio: datetime, fim: datetime) -> bool:
    """Verifica se o intervalo do atendimento está contido no horário de funcionamento.

    Args:
        inicio (datetime): Data e hora de início do atendimento.
        fim (datetime): Data e hora de término do atendimento.

    Returns:
        bool: True se o atendimento respeita o expediente, False caso contrário.
    """
    abertura = inicio.replace(hour=HORARIO_INICIO, minute=0, second=0, microsecond=0)
    fechamento = inicio.replace(hour=HORARIO_FIM, minute=0, second=0, microsecond=0)
    return inicio >= abertura and fim <= fechamento


def _ha_sobreposicao(inicio_a: datetime, fim_a: datetime, inicio_b: datetime, fim_b: datetime) -> bool:
    """Verifica se dois intervalos de tempo se sobrepõem.

    Utiliza a fórmula estrita: inicio_a < fim_b and inicio_b < fim_a.

    Args:
        inicio_a (datetime): Início do primeiro intervalo.
        fim_a (datetime): Fim do primeiro intervalo.
        inicio_b (datetime): Início do segundo intervalo.
        fim_b (datetime): Fim do segundo intervalo.

    Returns:
        bool: True se houver sobreposição entre os intervalos, False caso contrário.
    """
    return inicio_a < fim_b and inicio_b < fim_a


def _buscar_consulta(paciente: str, data: str, hora: int) -> Optional[Atendimento]:
    """Busca uma consulta agendada para um paciente em data e hora específicas.

    Args:
        paciente (str): Nome do paciente.
        data (str): Data da consulta no formato AAAA-MM-DD.
        hora (int): Hora da consulta.

    Returns:
        Optional[Atendimento]: Objeto do atendimento se encontrado, ou None caso contrário.
    """
    for consulta in agenda:
        if (
            consulta.paciente == paciente
            and consulta.data == data
            and consulta.hora == hora
        ):
            return consulta
    return None


def _verificar_disponibilidade(
    profissional: str,
    paciente: str,
    inicio: datetime,
    duracao: int,
    consulta_ignorada: Optional[Atendimento] = None,
) -> bool:
    """Verifica a disponibilidade de horário tanto para o profissional quanto para o paciente.

    Args:
        profissional (str): Nome do profissional responsável.
        paciente (str): Nome do paciente.
        inicio (datetime): Horário de início proposto.
        duracao (int): Duração em minutos da consulta proposta.
        consulta_ignorada (Optional[Atendimento]): Consulta que deve ser desconsiderada
            na verificação (útil em remarcações).

    Returns:
        bool: True se o horário estiver disponível, False se houver sobreposição.
    """
    fim = inicio + timedelta(minutes=duracao)

    for consulta in agenda:
        if consulta is consulta_ignorada:
            continue

        if _ha_sobreposicao(inicio, fim, consulta.inicio, consulta.fim):
            if consulta.profissional == profissional or consulta.paciente == paciente:
                return False

    return True


def marcar_consulta(
    paciente: str,
    profissional: str,
    data: str,
    hora: int,
    duracao: int,
) -> Optional[Atendimento]:
    """Realiza a marcação de uma nova consulta na agenda.

    Valida os parâmetros de entrada, o horário de funcionamento da clínica
    e a disponibilidade do profissional e do paciente antes de agendar.

    Args:
        paciente (str): Nome do paciente.
        profissional (str): Nome do profissional responsável.
        data (str): Data desejada para a consulta no formato AAAA-MM-DD.
        hora (int): Horário de início da consulta (entre 0 e 23).
        duracao (int): Duração da consulta em minutos (deve ser > 0).

    Returns:
        Optional[Atendimento]: Objeto do atendimento marcado, ou None se o horário estiver ocupado.

    Raises:
        ValueError: Se paciente ou profissional forem vazios, se a duração for <= 0,
            se o formato da data for inválido ou se a hora for inválida.
        HorarioInvalidoError: Se o atendimento estiver fora do horário de funcionamento
            da clínica (08:00 às 17:00).
    """
    # Cláusulas de guarda (pré-condições)
    if not paciente or not paciente.strip():
        raise ValueError(f"Nome do paciente não pode ser vazio. Valor informado: {paciente!r}")

    if not profissional or not profissional.strip():
        raise ValueError(f"Nome do profissional não pode ser vazio. Valor informado: {profissional!r}")

    if duracao <= 0:
        raise ValueError(f"Duração da consulta deve ser maior que zero minutos. Valor informado: {duracao}")

    if not _validar_data(data):
        raise ValueError(f"Data inválida ou em formato incorreto: '{data}'. Esperado formato AAAA-MM-DD.")

    if not (0 <= hora <= 23):
        raise ValueError(f"Hora de início inválida: {hora}. Deve estar entre 0 e 23.")

    inicio = datetime.strptime(f"{data} {hora:02d}:00", "%Y-%m-%d %H:%M")
    fim = inicio + timedelta(minutes=duracao)

    if not _dentro_do_expediente(inicio, fim):
        raise HorarioInvalidoError(
            f"Consulta das {inicio.strftime('%H:%M')} às {fim.strftime('%H:%M')} "
            f"ultrapassa o horário de expediente da clínica ({HORARIO_INICIO:02d}:00 às {HORARIO_FIM:02d}:00)."
        )

    if not _verificar_disponibilidade(profissional, paciente, inicio, duracao):
        _imprimir_mensagem("Horario ocupado")
        return None

    novo_atendimento = Atendimento(
        paciente=paciente.strip(),
        profissional=profissional.strip(),
        data=data,
        hora=hora,
        duracao=duracao,
    )
    agenda.append(novo_atendimento)
    _imprimir_mensagem(f"Atendimento marcado para {novo_atendimento.paciente}")
    return novo_atendimento


def remarcar_consulta(
    paciente: str,
    data: str,
    hora: int,
    nova_data: str,
    nova_hora: int,
) -> Optional[Atendimento]:
    """Remarca uma consulta existente para uma nova data e horário.

    Localiza a consulta original, valida o novo horário de acordo com o
    expediente e verifica sobreposição de horários antes de efetivar a mudança.

    Args:
        paciente (str): Nome do paciente.
        data (str): Data atual da consulta no formato AAAA-MM-DD.
        hora (int): Horário atual da consulta.
        nova_data (str): Nova data desejada no formato AAAA-MM-DD.
        nova_hora (int): Novo horário desejado (entre 0 e 23).

    Returns:
        Optional[Atendimento]: Objeto da consulta com dados atualizados, ou None se o horário estiver ocupado.

    Raises:
        ValueError: Se datas forem inválidas ou horas estiverem fora da faixa válida (0 a 23).
        ConsultaNaoEncontradaError: Se a consulta a ser remarcada não for encontrada na agenda.
        HorarioInvalidoError: Se o novo horário ultrapassar o expediente da clínica.
    """
    # Cláusulas de guarda (pré-condições)
    if not paciente or not paciente.strip():
        raise ValueError(f"Nome do paciente não pode ser vazio. Valor informado: {paciente!r}")

    if not _validar_data(data):
        raise ValueError(f"Data atual inválida: '{data}'. Esperado formato AAAA-MM-DD.")

    if not _validar_data(nova_data):
        raise ValueError(f"Nova data inválida: '{nova_data}'. Esperado formato AAAA-MM-DD.")

    if not (0 <= hora <= 23):
        raise ValueError(f"Hora atual inválida: {hora}. Deve estar entre 0 e 23.")

    if not (0 <= nova_hora <= 23):
        raise ValueError(f"Nova hora inválida: {nova_hora}. Deve estar entre 0 e 23.")

    consulta_atual = _buscar_consulta(paciente, data, hora)
    if consulta_atual is None:
        raise ConsultaNaoEncontradaError(
            f"Nenhuma consulta encontrada para o paciente '{paciente}' na data '{data}' às {hora:02d}:00."
        )

    novo_inicio = datetime.strptime(f"{nova_data} {nova_hora:02d}:00", "%Y-%m-%d %H:%M")
    novo_fim = novo_inicio + timedelta(minutes=consulta_atual.duracao)

    if not _dentro_do_expediente(novo_inicio, novo_fim):
        raise HorarioInvalidoError(
            f"Remarcação das {novo_inicio.strftime('%H:%M')} às {novo_fim.strftime('%H:%M')} "
            f"ultrapassa o horário de expediente da clínica ({HORARIO_INICIO:02d}:00 às {HORARIO_FIM:02d}:00)."
        )

    if not _verificar_disponibilidade(
        profissional=consulta_atual.profissional,
        paciente=paciente,
        inicio=novo_inicio,
        duracao=consulta_atual.duracao,
        consulta_ignorada=consulta_atual,
    ):
        _imprimir_mensagem("Horario ocupado")
        return None

    consulta_atual.data = nova_data
    consulta_atual.hora = nova_hora
    _imprimir_mensagem("Remarcado")
    return consulta_atual


def listar_atendimentos_do_dia(data: str) -> list[Atendimento]:
    """Lista no terminal todos os atendimentos agendados para uma data específica em ordem cronológica.

    Args:
        data (str): Data dos atendimentos a serem listados no formato AAAA-MM-DD.

    Returns:
        list[Atendimento]: Lista dos atendimentos agendados para o dia ordenados por horário.

    Raises:
        ValueError: Se a data informada for inválida ou não seguir o formato AAAA-MM-DD.
    """
    # Cláusula de guarda
    if not _validar_data(data):
        raise ValueError(f"Data inválida para listagem: '{data}'. Esperado formato AAAA-MM-DD.")

    atendimentos_do_dia = [
        atendimento for atendimento in agenda
        if atendimento.data == data
    ]
    atendimentos_do_dia.sort(key=lambda a: a.inicio)

    for atendimento in atendimentos_do_dia:
        _imprimir_mensagem(
            f"{atendimento.hora} {atendimento.paciente} {atendimento.profissional} {atendimento.status}"
        )

    return atendimentos_do_dia


if __name__ == "__main__":
    marcar_consulta("Ana", "Dr. Silva", "2026-10-05", 9, 30)
    marcar_consulta("Bruno", "Dr. Silva", "2026-10-05", 9, 30)
    marcar_consulta("Carla", "Dra. Souza", "2026-10-05", 14, 60)
    remarcar_consulta("Ana", "2026-10-05", 9, "2026-10-06", 10)
    listar_atendimentos_do_dia("2026-10-05")
