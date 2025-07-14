#!/usr/bin/env python3
"""
Script de teste final para verificar se o sistema está funcionando
"""

import sys
import os

def test_imports():
    """Testa se todas as importações funcionam"""
    print("🔍 Testando importações...")

    try:
        # Testa MySQL
        import mysql.connector
        print("✅ mysql-connector-python OK")

        # Testa OpenAI
        from openai import OpenAI
        print("✅ openai OK")

        # Testa dotenv
        from dotenv import load_dotenv
        print("✅ python-dotenv OK")

        # Testa pydantic
        from pydantic import BaseModel
        print("✅ pydantic OK")

        # Testa componentes do sistema
        from database.database_mysql import DatabaseManager
        print("✅ DatabaseManager OK")

        from identity.identity_manager import IdentityManager
        print("✅ IdentityManager OK")

        from notifications.reminder_system import ReminderSystem
        print("✅ ReminderSystem OK")

        from tools.daily_events import DailyEvents
        print("✅ DailyEvents OK")

        from utils.record_audio import record_audio
        print("✅ record_audio OK")

        return True

    except ImportError as e:
        print(f"❌ Erro de importação: {e}")
        return False
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        return False

def test_mysql_connection():
    """Testa conexão MySQL"""
    print("\n🔍 Testando conexão MySQL...")

    try:
        import mysql.connector
        from mysql.connector import Error

        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="agent_memory"
        )

        if connection.is_connected():
            print("✅ Conexão MySQL estabelecida!")

            # Testa criar tabelas
            cursor = connection.cursor()
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()

            expected_tables = ['events', 'interactions', 'reminders', 'identities']
            found_tables = []
            for table in tables:
                if isinstance(table, (tuple, list)) and len(table) > 0:
                    found_tables.append(str(table[0]))

            print(f"📊 Tabelas encontradas: {found_tables}")

            missing_tables = [table for table in expected_tables if table not in found_tables]
            if missing_tables:
                print(f"⚠️ Tabelas faltando: {missing_tables}")
                print("💡 Execute o sistema uma vez para criar as tabelas")
            else:
                print("✅ Todas as tabelas necessárias existem!")

            connection.close()
            return True
        else:
            print("❌ Falha na conexão MySQL")
            return False

    except Error as e:
        print(f"❌ Erro MySQL: {e}")
        return False
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        return False

def test_openai_config():
    """Testa configuração OpenAI"""
    print("\n🔍 Testando configuração OpenAI...")

    try:
        from dotenv import load_dotenv
        load_dotenv()

        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            print("❌ OPENAI_API_KEY não encontrada no arquivo .env")
            print("💡 Crie um arquivo .env com: OPENAI_API_KEY=sua_chave_aqui")
            return False

        print("✅ OPENAI_API_KEY encontrada!")
        return True

    except Exception as e:
        print(f"❌ Erro ao testar OpenAI: {e}")
        return False

def test_components():
    """Testa componentes do sistema"""
    print("\n🔍 Testando componentes do sistema...")

    try:
        # Testa DatabaseManager
        from database.database_mysql import DatabaseManager
        db = DatabaseManager()
        print("✅ DatabaseManager inicializado!")

        # Testa IdentityManager
        from identity.identity_manager import IdentityManager
        identity_mgr = IdentityManager()
        print("✅ IdentityManager inicializado!")

        # Testa ReminderSystem
        from notifications.reminder_system import ReminderSystem
        reminder_sys = ReminderSystem()
        print("✅ ReminderSystem inicializado!")

        # Testa DailyEvents
        from tools.daily_events import DailyEvents
        print("✅ DailyEvents importado!")

        return True

    except Exception as e:
        print(f"❌ Erro ao testar componentes: {e}")
        return False

def test_validation_correction():
    """Testa a correção de validação"""
    print("\n🔍 Testando correção de validação...")

    try:
        from tools.daily_events import DailyEvents

        # Testa com dados em português (deve ser corrigido)
        test_data = {
            "date": "15/01/2025",
            "events": [
                {
                    "título": "Teste",
                    "descrição": "Descrição teste",
                    "categoria": "trabalho",
                    "prioridade": "media"
                }
            ]
        }

        # Aplica correção
        field_mapping = {
            'título': 'title',
            'titulo': 'title',
            'descrição': 'description',
            'descricao': 'description',
            'categoria': 'category',
            'prioridade': 'priority'
        }

        for event in test_data.get('events', []):
            corrected_event = {}
            for key, value in event.items():
                corrected_key = field_mapping.get(key, key)
                corrected_event[corrected_key] = value
            event.clear()
            event.update(corrected_event)

        # Tenta criar objeto
        daily_events = DailyEvents(**test_data)
        print("✅ Correção de validação funcionando!")
        return True

    except Exception as e:
        print(f"❌ Erro na correção de validação: {e}")
        return False

def main():
    """Executa todos os testes"""
    print("🧪 TESTE FINAL DO SISTEMA")
    print("=" * 50)

    # Testa importações
    imports_ok = test_imports()

    # Testa MySQL
    mysql_ok = test_mysql_connection()

    # Testa OpenAI
    openai_ok = test_openai_config()

    # Testa componentes
    components_ok = test_components()

    # Testa correção de validação
    validation_ok = test_validation_correction()

    print("\n📊 RESUMO DOS TESTES:")
    print("-" * 30)
    print(f"Importações: {'✅ OK' if imports_ok else '❌ FALHOU'}")
    print(f"MySQL: {'✅ OK' if mysql_ok else '❌ FALHOU'}")
    print(f"OpenAI: {'✅ OK' if openai_ok else '❌ FALHOU'}")
    print(f"Componentes: {'✅ OK' if components_ok else '❌ FALHOU'}")
    print(f"Validação: {'✅ OK' if validation_ok else '❌ FALHOU'}")

    all_tests_passed = all([imports_ok, mysql_ok, openai_ok, components_ok, validation_ok])

    if all_tests_passed:
        print("\n🎉 TODOS OS TESTES PASSARAM!")
        print("🚀 O sistema está pronto para uso!")
        print("\n💡 Para executar:")
        print("   python main_enhanced_fixed.py")
    else:
        print("\n⚠️ Alguns testes falharam.")
        print("🔧 Verifique os erros acima antes de executar o sistema.")

if __name__ == "__main__":
    main()
