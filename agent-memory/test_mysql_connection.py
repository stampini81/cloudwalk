#!/usr/bin/env python3
"""
Script de teste para verificar a conexão MySQL e componentes do sistema
"""

import sys
import os

def test_mysql_connection():
    """Testa a conexão com MySQL"""
    try:
        import mysql.connector
        from mysql.connector import Error

        print("🔍 Testando conexão MySQL...")

        # Tenta conectar
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="agent_memory"
        )

        if connection.is_connected():
            print("✅ Conexão MySQL estabelecida com sucesso!")

            # Testa criar tabelas
            cursor = connection.cursor()

            # Testa tabela events
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS test_events (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    title VARCHAR(255) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            # Insere teste
            cursor.execute('''
                INSERT INTO test_events (title) VALUES (%s)
            ''', ("Teste de conexão",))

            # Busca teste
            cursor.execute('SELECT * FROM test_events WHERE title = %s', ("Teste de conexão",))
            result = cursor.fetchone()

            if result:
                print("✅ Inserção e busca funcionando!")

            # Limpa teste
            cursor.execute('DELETE FROM test_events WHERE title = %s', ("Teste de conexão",))

            connection.commit()
            connection.close()

            return True
        else:
            print("❌ Falha na conexão MySQL")
            return False

    except ImportError:
        print("❌ mysql-connector-python não instalado")
        print("💡 Execute: pip install mysql-connector-python")
        return False
    except Error as e:
        print(f"❌ Erro MySQL: {e}")
        return False
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        return False

def test_components():
    """Testa os componentes do sistema"""
    print("\n🔍 Testando componentes do sistema...")

    try:
        # Testa DatabaseManager
        print("📊 Testando DatabaseManager...")
        from database.database_mysql import DatabaseManager
        db = DatabaseManager()
        print("✅ DatabaseManager OK!")

        # Testa IdentityManager
        print("👥 Testando IdentityManager...")
        from identity.identity_manager import IdentityManager
        identity_mgr = IdentityManager()
        print("✅ IdentityManager OK!")

        # Testa ReminderSystem
        print("🔔 Testando ReminderSystem...")
        from notifications.reminder_system import ReminderSystem
        reminder_sys = ReminderSystem()
        print("✅ ReminderSystem OK!")

        # Testa DailyEvents
        print("📅 Testando DailyEvents...")
        from tools.daily_events import DailyEvents
        print("✅ DailyEvents OK!")

        # Testa record_audio
        print("🎤 Testando record_audio...")
        from utils.record_audio import record_audio
        print("✅ record_audio OK!")

        return True

    except Exception as e:
        print(f"❌ Erro ao testar componentes: {e}")
        return False

def test_openai():
    """Testa a configuração da OpenAI"""
    print("\n🔍 Testando configuração OpenAI...")

    try:
        from dotenv import load_dotenv
        load_dotenv()

        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            print("❌ OPENAI_API_KEY não encontrada no arquivo .env")
            return False

        print("✅ OPENAI_API_KEY encontrada!")
        return True

    except Exception as e:
        print(f"❌ Erro ao testar OpenAI: {e}")
        return False

def main():
    """Executa todos os testes"""
    print("🧪 TESTE DE CONFIGURAÇÃO DO SISTEMA")
    print("=" * 50)

    # Testa MySQL
    mysql_ok = test_mysql_connection()

    # Testa componentes
    components_ok = test_components()

    # Testa OpenAI
    openai_ok = test_openai()

    print("\n📊 RESUMO DOS TESTES:")
    print("-" * 30)
    print(f"MySQL: {'✅ OK' if mysql_ok else '❌ FALHOU'}")
    print(f"Componentes: {'✅ OK' if components_ok else '❌ FALHOU'}")
    print(f"OpenAI: {'✅ OK' if openai_ok else '❌ FALHOU'}")

    if mysql_ok and components_ok and openai_ok:
        print("\n🎉 Todos os testes passaram! O sistema está pronto para uso.")
        print("\n💡 Para executar o sistema:")
        print("   python main_enhanced_fixed.py")
    else:
        print("\n⚠️ Alguns testes falharam. Verifique os erros acima.")

        if not mysql_ok:
            print("\n🔧 Para corrigir MySQL:")
            print("   1. Instale: pip install mysql-connector-python")
            print("   2. Crie o banco: CREATE DATABASE agent_memory;")
            print("   3. Verifique se o XAMPP está rodando")

        if not openai_ok:
            print("\n🔧 Para corrigir OpenAI:")
            print("   1. Crie arquivo .env com: OPENAI_API_KEY=sua_chave_aqui")

if __name__ == "__main__":
    main()
