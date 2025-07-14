#!/usr/bin/env python3
"""
Script de teste para verificar a correção de validação
"""

import json
from tools.daily_events import DailyEvents

def test_field_mapping():
    """Testa o mapeamento de campos de português para inglês"""

    # Simula dados da IA com campos em português
    ai_data_with_portuguese = {
        "date": "15/01/2025",
        "events": [
            {
                "título": "Visita a Garcia",
                "descrição": "Estadia em Garcia para trabalho",
                "categoria": "trabalho",
                "prioridade": "media",
                "local": "Garcia, SP"
            },
            {
                "título": "Visita a Marília",
                "descrição": "Estadia em Marília para trabalho",
                "categoria": "trabalho",
                "prioridade": "media",
                "local": "Marília, SP"
            }
        ]
    }

    print("🔍 Testando mapeamento de campos...")
    print(f"Dados originais: {json.dumps(ai_data_with_portuguese, indent=2)}")

    # Aplica correção de campos
    field_mapping = {
        'título': 'title',
        'titulo': 'title',
        'descrição': 'description',
        'descricao': 'description',
        'categoria': 'category',
        'prioridade': 'priority',
        'horário': 'time',
        'horario': 'time',
        'local': 'location',
        'lembrete': 'reminder'
    }

    # Corrige campos
    for event in ai_data_with_portuguese.get('events', []):
        corrected_event = {}
        for key, value in event.items():
            corrected_key = field_mapping.get(key, key)
            corrected_event[corrected_key] = value

        # Atualiza o evento
        event.clear()
        event.update(corrected_event)

    print(f"Dados corrigidos: {json.dumps(ai_data_with_portuguese, indent=2)}")

    try:
        # Tenta criar objeto DailyEvents
        daily_events = DailyEvents(**ai_data_with_portuguese)
        print("✅ Validação passou! Objeto DailyEvents criado com sucesso.")
        print(f"Eventos processados: {len(daily_events.events)}")

        for i, event in enumerate(daily_events.events):
            print(f"  Evento {i+1}: {event.title} - {event.description}")

        return True

    except Exception as e:
        print(f"❌ Erro na validação: {e}")
        return False

def test_english_fields():
    """Testa com campos em inglês (deve funcionar)"""

    ai_data_english = {
        "date": "15/01/2025",
        "events": [
            {
                "title": "Visit to Garcia",
                "description": "Stay in Garcia for work",
                "category": "trabalho",
                "priority": "media",
                "location": "Garcia, SP"
            }
        ]
    }

    print("\n🔍 Testando campos em inglês...")

    try:
        daily_events = DailyEvents(**ai_data_english)
        print("✅ Campos em inglês funcionam corretamente!")
        return True
    except Exception as e:
        print(f"❌ Erro com campos em inglês: {e}")
        return False

if __name__ == "__main__":
    print("🧪 TESTE DE CORREÇÃO DE VALIDAÇÃO")
    print("=" * 50)

    # Testa mapeamento de campos
    mapping_ok = test_field_mapping()

    # Testa campos em inglês
    english_ok = test_english_fields()

    print("\n📊 RESUMO:")
    print("-" * 30)
    print(f"Mapeamento de campos: {'✅ OK' if mapping_ok else '❌ FALHOU'}")
    print(f"Campos em inglês: {'✅ OK' if english_ok else '❌ FALHOU'}")

    if mapping_ok and english_ok:
        print("\n🎉 Correção de validação funcionando!")
        print("💡 O sistema deve processar eventos corretamente agora.")
    else:
        print("\n⚠️ Ainda há problemas com a validação.")
