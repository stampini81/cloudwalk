from pydantic import BaseModel, Field
from typing import List

class DailyEvents(BaseModel):
    """
    Identifica e registra eventos diários para salvar em uma planilha.
    
    Args:
        date (str): Data em que os eventos devem ser identificados, no formato YYYY-MM-DD
        events (List[Event]): Lista de eventos identificados no dia, cada um contendo título, 
            descrição e horário

    Returns:
        str: Confirmação do registro dos eventos
    """
    
    date: str = Field(
        description="Data em que os eventos ocorreram no formato DD/MM/YYYY"
    )
        
    events: List[str] = Field(
        description="Lista de eventos identificados no dia"
    )
