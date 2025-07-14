#!/usr/bin/env python3
"""
Script para visualizar dados do banco de dados MySQL
"""

import mysql.connector
from mysql.connector import Error
import json
from datetime import datetime
from typing import List, Dict, Any, cast

def view_database(host="localhost", user="root", password="", database="agent_memory"):
    """Visualiza todos os dados do banco de dados"""

    try:
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        cursor = connection.cursor()

        print("🔍 VISUALIZADOR DO BANCO DE DADOS")
        print("=" * 50)

        # Verifica se o banco existe e tem dados
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()

        if not tables:
            print("❌ Nenhuma tabela encontrada no banco de dados")
            return

        table_names = []
        for table in tables:
            if isinstance(table, (tuple, list)) and len(table) > 0:
                table_names.append(str(table[0]))
        print(f"📊 Tabelas encontradas: {table_names}")
        print()

        # Visualiza eventos
        print("📅 EVENTOS SALVOS:")
        print("-" * 30)
        cursor.execute("SELECT * FROM events ORDER BY created_at DESC LIMIT 10")
        events = cursor.fetchall()

        if events:
            for event in events:
                event_data = cast(Any, event)
                print(f"ID: {event_data[0]}")
                print(f"Data: {event_data[1]}")
                print(f"Título: {event_data[2]}")
                print(f"Descrição: {event_data[3]}")
                print(f"Categoria: {event_data[4]}")
                print(f"Prioridade: {event_data[5]}")
                print(f"Horário: {event_data[6]}")
                print(f"Local: {event_data[7]}")
                print(f"Lembrete: {event_data[8]}")
                print(f"Criado em: {event_data[9]}")
                print("-" * 20)
        else:
            print("❌ Nenhum evento encontrado")

        print()

        # Visualiza interações
        print("💬 INTERAÇÕES RECENTES:")
        print("-" * 30)
        cursor.execute("SELECT * FROM interactions ORDER BY timestamp DESC LIMIT 5")
        interactions = cursor.fetchall()

        if interactions:
            for interaction in interactions:
                interaction_data = cast(Any, interaction)
                print(f"ID: {interaction_data[0]}")
                print(f"Timestamp: {interaction_data[1]}")
                print(f"Você disse: {interaction_data[2]}")
                print(f"Assistente: {interaction_data[3]}")
                print(f"Contexto: {interaction_data[4]}")
                print("-" * 20)
        else:
            print("❌ Nenhuma interação encontrada")

        print()

        # Visualiza lembretes
        print("🔔 LEMBRETES:")
        print("-" * 30)
        cursor.execute("SELECT * FROM reminders ORDER BY created_at DESC LIMIT 5")
        reminders = cursor.fetchall()

        if reminders:
            for reminder in reminders:
                reminder_data = cast(Any, reminder)
                print(f"ID: {reminder_data[0]}")
                print(f"Evento ID: {reminder_data[1]}")
                print(f"Horário do lembrete: {reminder_data[2]}")
                print(f"Mensagem: {reminder_data[3]}")
                print(f"Enviado: {reminder_data[4]}")
                print(f"Criado em: {reminder_data[5]}")
                print("-" * 20)
        else:
            print("❌ Nenhum lembrete encontrado")

        print()

        # Visualiza identidades
        print("👥 IDENTIDADES:")
        print("-" * 30)
        cursor.execute("SELECT * FROM identities ORDER BY created_at DESC LIMIT 5")
        identities = cursor.fetchall()

        if identities:
            for identity in identities:
                identity_data = cast(Any, identity)
                print(f"ID: {identity_data[0]}")
                print(f"Nome: {identity_data[1]}")
                print(f"Papel: {identity_data[2]}")
                print(f"Relacionamento: {identity_data[3]}")
                print(f"Preferências: {identity_data[4]}")
                print(f"Notas: {identity_data[5]}")
                print(f"Criado em: {identity_data[6]}")
                print("-" * 20)
        else:
            print("❌ Nenhuma identidade encontrada")

        # Estatísticas gerais
        print()
        print("📊 ESTATÍSTICAS:")
        print("-" * 30)

        cursor.execute("SELECT COUNT(*) FROM events")
        result = cursor.fetchone()
        total_events = result[0] if result and isinstance(result, (tuple, list)) and len(result) > 0 else 0
        print(f"Total de eventos: {total_events}")

        cursor.execute("SELECT COUNT(*) FROM interactions")
        result = cursor.fetchone()
        total_interactions = result[0] if result and isinstance(result, (tuple, list)) and len(result) > 0 else 0
        print(f"Total de interações: {total_interactions}")

        cursor.execute("SELECT COUNT(*) FROM reminders")
        result = cursor.fetchone()
        total_reminders = result[0] if result and isinstance(result, (tuple, list)) and len(result) > 0 else 0
        print(f"Total de lembretes: {total_reminders}")

        cursor.execute("SELECT COUNT(*) FROM identities")
        result = cursor.fetchone()
        total_identities = result[0] if result and isinstance(result, (tuple, list)) and len(result) > 0 else 0
        print(f"Total de identidades: {total_identities}")

        connection.close()

    except Error as e:
        print(f"❌ Erro ao acessar banco de dados: {e}")

def export_to_json(host="localhost", user="root", password="", database="agent_memory", output_file="database_export.json"):
    """Exporta dados do banco para JSON"""

    try:
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        cursor = connection.cursor()

        data = {
            'events': [],
            'interactions': [],
            'reminders': [],
            'identities': []
        }

        # Exporta eventos
        cursor.execute("SELECT * FROM events")
        events = cursor.fetchall()
        for event in events:
            event_data = cast(Any, event)
            data['events'].append({
                'id': event_data[0],
                'date': event_data[1],
                'title': event_data[2],
                'description': event_data[3],
                'category': event_data[4],
                'priority': event_data[5],
                'time': event_data[6],
                'location': event_data[7],
                'reminder': event_data[8],
                'created_at': str(event_data[9]) if event_data[9] else None,
                'updated_at': str(event_data[10]) if event_data[10] else None
            })

        # Exporta interações
        cursor.execute("SELECT * FROM interactions")
        interactions = cursor.fetchall()
        for interaction in interactions:
            interaction_data = cast(Any, interaction)
            data['interactions'].append({
                'id': interaction_data[0],
                'timestamp': str(interaction_data[1]) if interaction_data[1] else None,
                'human_message': interaction_data[2],
                'assistant_message': interaction_data[3],
                'context': interaction_data[4]
            })

        # Exporta lembretes
        cursor.execute("SELECT * FROM reminders")
        reminders = cursor.fetchall()
        for reminder in reminders:
            reminder_data = cast(Any, reminder)
            data['reminders'].append({
                'id': reminder_data[0],
                'event_id': reminder_data[1],
                'reminder_time': str(reminder_data[2]) if reminder_data[2] else None,
                'message': reminder_data[3],
                'is_sent': bool(reminder_data[4]),
                'created_at': str(reminder_data[5]) if reminder_data[5] else None
            })

        # Exporta identidades
        cursor.execute("SELECT * FROM identities")
        identities = cursor.fetchall()
        for identity in identities:
            identity_data = cast(Any, identity)
            data['identities'].append({
                'id': identity_data[0],
                'name': identity_data[1],
                'role': identity_data[2],
                'relationship': identity_data[3],
                'preferences': identity_data[4],
                'notes': identity_data[5],
                'created_at': str(identity_data[6]) if identity_data[6] else None,
                'updated_at': str(identity_data[7]) if identity_data[7] else None
            })

        connection.close()

        # Salva no arquivo JSON
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        print(f"✅ Dados exportados para {output_file}")

    except Error as e:
        print(f"❌ Erro ao exportar dados: {e}")

if __name__ == "__main__":
    print("🔍 VISUALIZADOR DO BANCO DE DADOS MySQL")
    print("=" * 50)

    # Visualiza dados
    view_database()

    print()
    print("💾 Deseja exportar os dados para JSON? (s/n): ", end="")
    response = input().lower()

    if response in ['s', 'sim', 'y', 'yes']:
        export_to_json()
        print("📄 Arquivo JSON criado com sucesso!")

    print("\n✅ Visualização concluída!")
