from openai import OpenAI
from dotenv import load_dotenv
from dotenv import find_dotenv
import os
from utils.record_audio import record_audio
from utils.basemodel2tool import base_model2tool
from tools.daily_events import DailyEvents
from database.database import DatabaseManager
from notifications.reminder_system import ReminderSystem
from identity.identity_manager import IdentityManager
from datetime import datetime
import json
import threading
import time
from typing import Dict, Any, Optional

# Carrega variáveis de ambiente
load_dotenv(find_dotenv())

class EnhancedMemoryAssistant:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.db_manager = DatabaseManager()
        self.reminder_system = ReminderSystem()
        self.identity_manager = IdentityManager()

        # Inicia sistema de lembretes
        self.reminder_system.start()

        print("🚀 Assistente de Memória Avançado Iniciado!")
        print("💡 Funcionalidades:")
        print("   📊 Categorização de eventos")
        print("   🔔 Sistema de lembretes")
        print("   👥 Reconhecimento de identidades")
        print("   💾 Persistência com banco de dados")
        print("   🎤 Interface por voz")
        print("-" * 50)

    def process_audio(self, filename_audio: str) -> str:
        """Processa áudio e retorna transcrição"""
        try:
            with open(filename_audio, "rb") as audio_file:
                transcription = self.client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    language="pt"
                )

            # Aguarda um pouco antes de tentar deletar o arquivo
            time.sleep(0.5)

            try:
                os.remove(filename_audio)
            except PermissionError:
                print(f"⚠️ Não foi possível deletar {filename_audio} - arquivo ainda em uso")
                time.sleep(1)
                try:
                    os.remove(filename_audio)
                except PermissionError:
                    print(f"⚠️ Arquivo {filename_audio} não foi deletado automaticamente")

            return transcription.text

        except Exception as e:
            print(f"❌ Erro ao processar áudio: {e}")
            return ""

    def extract_identities(self, text: str) -> list:
        """Extrai identidades do texto"""
        return self.identity_manager.extract_identities_from_text(text)

    def get_context(self) -> Dict[str, Any]:
        """Obtém contexto completo da memória"""
        memory_context = self.db_manager.get_memory_context()
        identity_context = self.identity_manager.get_all_contexts()

        return {
            'memory': memory_context,
            'identities': identity_context
        }

    def process_with_ai(self, text: str, context: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Processa texto com IA usando contexto completo"""
        actual_date = datetime.now().strftime("%d/%m/%Y")

        # Constrói prompt com contexto
        context_prompt = f"""
        Você é um assistente de memória pessoal avançado. Hoje é {actual_date}.

        CONTEXTO DA MEMÓRIA:
        {json.dumps(context['memory'], indent=2, ensure_ascii=False)}

        IDENTIDADES CONHECIDAS:
        {context['identities']}

        INSTRUÇÕES IMPORTANTES:
        1. Identifique e categorize eventos mencionados
        2. Use APENAS estas categorias: trabalho, saude, pessoal, familia, lazer, estudos, financeiro, outros
        3. Use APENAS estas prioridades: baixa, media, alta, urgente
        4. Reconheça pessoas e relacionamentos
        5. Sugira lembretes apropriados (ex: "30min antes", "1h antes", "1 dia antes")
        6. Use linguagem natural e contextualizada
        7. Seja útil e proativo

        EXEMPLOS DE CATEGORIZAÇÃO:
        - "reunião" → categoria: trabalho
        - "viagem" → categoria: lazer
        - "consulta médica" → categoria: saude
        - "estudar" → categoria: estudos
        - "família" → categoria: familia
        - "conta" → categoria: financeiro
        """

        try:
            completion = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": context_prompt},
                    {"role": "user", "content": text}
                ],
                tool_choice="auto",
                tools=[base_model2tool(DailyEvents)]  # type: ignore
            )

            return {
                'completion': completion,
                'text': text,
                'context': context
            }

        except Exception as e:
            print(f"❌ Erro ao processar com IA: {e}")
            return None

    def save_events(self, events_data: Dict[str, Any]) -> bool:
        """Salva eventos no banco de dados"""
        try:
            # Salva eventos
            success = self.db_manager.save_events(events_data)

            if success and events_data.get('events'):
                # Cria lembretes para eventos com reminder
                for event in events_data['events']:
                    if event.get('reminder'):
                        # Aqui você implementaria a criação de lembretes
                        print(f"🔔 Lembrete configurado para: {event.get('title')}")

            return success

        except Exception as e:
            print(f"❌ Erro ao salvar eventos: {e}")
            return False

    def save_interaction(self, human_message: str, assistant_message: str) -> None:
        """Salva interação no banco de dados"""
        self.db_manager.save_interaction(human_message, assistant_message)

    def run(self) -> None:
        """Executa o loop principal do assistente"""
        print("🎤 Diga 'sair' para encerrar a aplicação")
        print("-" * 50)

        while True:
            try:
                # Grava áudio
                filename_audio = record_audio()
                if not filename_audio:
                    print("❌ Erro ao gravar áudio")
                    continue

                # Processa áudio
                text = self.process_audio(filename_audio)
                if not text:
                    continue

                text = text.lower().strip()
                print(f"🎤 Você disse: {text}")

                # Verifica comando de saída
                if text in ["sair", "quit", "exit", "encerrar", "parar"]:
                    print("👋 Encerrando aplicação...")
                    self.reminder_system.stop()
                    break

                # Extrai identidades
                identities = self.extract_identities(text)
                if identities:
                    print(f"👥 Identidades reconhecidas: {len(identities)}")

                # Obtém contexto
                context = self.get_context()

                # Processa com IA
                result = self.process_with_ai(text, context)
                if not result:
                    continue

                completion = result['completion']

                # Processa resposta da IA
                if completion.choices[0].message.tool_calls:
                    for tool_call in completion.choices[0].message.tool_calls:
                        if tool_call.function.name == "DailyEvents":
                            try:
                                # Obtém dados da IA
                                ai_data = json.loads(tool_call.function.arguments)

                                # Mapeia valores da IA para nossas enumerações
                                for event in ai_data.get('events', []):
                                    # Mapeia categoria
                                    category_mapping = {
                                        'viagem': 'lazer',
                                        'travel': 'lazer',
                                        'trip': 'lazer',
                                        'reunião': 'trabalho',
                                        'meeting': 'trabalho',
                                        'consulta': 'saude',
                                        'appointment': 'saude',
                                        'médico': 'saude',
                                        'doctor': 'saude',
                                        'estudo': 'estudos',
                                        'study': 'estudos',
                                        'curso': 'estudos',
                                        'course': 'estudos',
                                        'família': 'familia',
                                        'family': 'familia',
                                        'pessoal': 'pessoal',
                                        'personal': 'pessoal',
                                        'financeiro': 'financeiro',
                                        'financial': 'financeiro',
                                        'conta': 'financeiro',
                                        'bill': 'financeiro'
                                    }

                                    if 'category' in event:
                                        ai_category = event['category'].lower()
                                        event['category'] = category_mapping.get(ai_category, 'outros')

                                    # Mapeia prioridade
                                    priority_mapping = {
                                        'normal': 'media',
                                        'regular': 'media',
                                        'usual': 'media',
                                        'importante': 'alta',
                                        'important': 'alta',
                                        'urgente': 'urgente',
                                        'urgent': 'urgente',
                                        'baixa': 'baixa',
                                        'low': 'baixa'
                                    }

                                    if 'priority' in event:
                                        ai_priority = event['priority'].lower()
                                        event['priority'] = priority_mapping.get(ai_priority, 'media')

                                # Cria objeto DailyEvents com dados corrigidos
                                daily_events = DailyEvents(**ai_data)

                                # Converte para formato do banco
                                events_data = {
                                    'date': daily_events.date,
                                    'events': [
                                        {
                                            'title': event.title,
                                            'description': event.description,
                                            'category': event.category.value,
                                            'priority': event.priority.value,
                                            'time': event.time,
                                            'location': event.location,
                                            'reminder': event.reminder
                                        }
                                        for event in daily_events.events
                                    ]
                                }

                                # Salva eventos
                                if self.save_events(events_data):
                                    print(f"✅ Eventos do dia {daily_events.date} registrados com sucesso!")

                                    # Resposta contextualizada
                                    response = f"Perfeito! Registrei {len(daily_events.events)} evento(s) para {daily_events.date}.\n"

                                    for event in daily_events.events:
                                        category_emoji = self.get_category_emoji(event.category.value)
                                        priority_emoji = self.get_priority_emoji(event.priority.value)
                                        response += f"{category_emoji} {priority_emoji} {event.title}\n"

                                    if any(event.reminder for event in daily_events.events):
                                        response += "\n🔔 Lembretes configurados automaticamente!"

                                    print(response)
                                    self.save_interaction(text, response)
                                else:
                                    print("❌ Erro ao salvar eventos")

                            except Exception as e:
                                print(f"❌ Erro ao processar eventos: {e}")
                                print("💡 Tentando processar como conversa normal...")
                                # Continua para processar como mensagem normal

                if completion.choices[0].message.content:
                    response = completion.choices[0].message.content
                    print(f"🤖 {response}")
                    self.save_interaction(text, response)

            except KeyboardInterrupt:
                print("\n👋 Encerrando aplicação...")
                self.reminder_system.stop()
                break
            except Exception as e:
                print(f"❌ Erro inesperado: {e}")
                continue

    def get_category_emoji(self, category: str) -> str:
        """Retorna emoji para categoria"""
        emojis = {
            'trabalho': '💼',
            'saude': '🏥',
            'pessoal': '👤',
            'familia': '👨‍👩‍👧‍👦',
            'lazer': '🎮',
            'estudos': '📚',
            'financeiro': '💰',
            'outros': '📌'
        }
        return emojis.get(category, '📌')

    def get_priority_emoji(self, priority: str) -> str:
        """Retorna emoji para prioridade"""
        emojis = {
            'baixa': '🟢',
            'media': '🟡',
            'alta': '🟠',
            'urgente': '🔴'
        }
        return emojis.get(priority, '🟡')

if __name__ == "__main__":
    assistant = EnhancedMemoryAssistant()
    assistant.run()
