from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum

class EventCategory(str, Enum):
    """Categorias de eventos disponíveis"""
    TRABALHO = "trabalho"
    SAUDE = "saude"
    PESSOAL = "pessoal"
    FAMILIA = "familia"
    LAZER = "lazer"
    ESTUDOS = "estudos"
    FINANCEIRO = "financeiro"
    OUTROS = "outros"

class EventPriority(str, Enum):
    """Prioridades de eventos"""
    BAIXA = "baixa"
    MEDIA = "media"
    ALTA = "alta"
    URGENTE = "urgente"

class Event(BaseModel):
    """Modelo para um evento individual"""
    title: str = Field(description="Título do evento")
    description: str = Field(description="Descrição detalhada do evento")
    category: EventCategory = Field(default=EventCategory.OUTROS, description="Categoria do evento")
    priority: EventPriority = Field(default=EventPriority.MEDIA, description="Prioridade do evento")
    time: Optional[str] = Field(default=None, description="Horário do evento (HH:MM)")
    location: Optional[str] = Field(default=None, description="Local do evento")
    reminder: Optional[str] = Field(default=None, description="Lembrete (ex: 30min antes, 1h antes)")

class DailyEvents(BaseModel):
    """
    Identifica e registra eventos diários categorizados para salvar em banco de dados.

    Args:
        date (str): Data em que os eventos ocorreram no formato DD/MM/YYYY
        events (List[Event]): Lista de eventos identificados no dia, cada um contendo título,
            descrição, categoria, prioridade e outros detalhes

    Returns:
        str: Confirmação do registro dos eventos
    """

    date: str = Field(
        description="Data em que os eventos ocorreram no formato DD/MM/YYYY"
    )

    events: List[Event] = Field(
        description="Lista de eventos identificados no dia com categorização"
    )
