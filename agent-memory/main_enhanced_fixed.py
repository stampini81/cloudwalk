from openai import OpenAI
from dotenv import load_dotenv
from dotenv import find_dotenv
import os
from utils.record_audio import record_audio
from utils.basemodel2tool import base_model2tool
from tools.daily_events import DailyEvents
# Requer: pip install mysql-connector-python
from database.database_mysql import DatabaseManager
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
            error_msg = str(e)
            if "audio_too_short" in error_msg:
                print("⚠️ Gravação muito curta para processamento. Tente gravar por mais tempo.")
            elif "rate_limit" in error_msg.lower():
                print("⚠️ Limite de requisições excedido. Aguarde um momento.")
            elif "quota" in error_msg.lower():
                print("⚠️ Cota da API excedida. Verifique suas credenciais.")
            else:
                print(f"❌ Erro ao processar áudio: {e}")

            # Tenta deletar o arquivo mesmo em caso de erro
            try:
                if os.path.exists(filename_audio):
                    os.remove(filename_audio)
            except:
                pass

            return ""

    def get_context(self) -> Dict[str, Any]:
        """Obtém contexto completo da memória"""
        memory_context = self.db_manager.get_memory_context()
        identity_context = self.identity_manager.get_all_contexts()

        # Converte objetos datetime para string para serialização JSON
        def convert_datetime(obj):
            if isinstance(obj, datetime):
                return obj.isoformat()
            elif isinstance(obj, dict):
                return {k: convert_datetime(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [convert_datetime(item) for item in obj]
            return obj

        return {
            'memory': convert_datetime(memory_context),
            'identities': convert_datetime(identity_context)
        }

    def process_with_ai(self, text: str, context: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Processa texto com IA usando prompt simplificado"""
        actual_date = datetime.now().strftime("%d/%m/%Y")

        # Prompt simplificado baseado no main.py original
        system_prompt = f"""You are a helpful assistant responsible for remembering events of my life. Today is {actual_date}. Use this as a reference to remember events. If the event occurred in the past, you should use the date to remember the event using today's date as a reference.

When the user mentions events, dates, activities, or locations, ALWAYS use the DailyEvents tool to record them properly.

IMPORTANT: Use ONLY English field names in the DailyEvents tool:
- title (not título)
- description (not descrição)
- category (not categoria)
- priority (not prioridade)
- time (not horário)
- location (not local)
- reminder (not lembrete)

Available categories: trabalho, saude, pessoal, familia, lazer, estudos, financeiro, outros
Available priorities: baixa, media, alta, urgente

Use the DailyEvents tool whenever events are mentioned."""

        try:
            completion = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "assistant", "content": json.dumps(context['memory'], default=str)},
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
                    print("⚠️ Gravação muito curta. Tente novamente.")
                    continue

                # Processa áudio
                text = self.process_audio(filename_audio)
                if not text:
                    print("❌ Erro ao processar áudio")
                    continue

                text = text.lower().strip()
                print(f"🎤 Você disse: {text}")

                # Verifica comando de saída
                exit_commands = ["sair", "quit", "exit", "encerrar", "parar"]
                if any(cmd in text for cmd in exit_commands):
                    print("👋 Encerrando aplicação...")
                    self.reminder_system.stop()
                    break

                # Obtém contexto
                context = self.get_context()

                # Processa com IA
                result = self.process_with_ai(text, context)
                if not result:
                    continue

                completion = result['completion']

                # Processa resposta da IA
                if completion.choices[0].message.tool_calls:
                    print("🔧 Processando eventos...")
                    for tool_call in completion.choices[0].message.tool_calls:
                        if tool_call.function.name == "DailyEvents":
                            try:
                                # Obtém dados da IA
                                ai_data = json.loads(tool_call.function.arguments)

                                # Verifica se há eventos na resposta
                                if 'events' not in ai_data or not ai_data['events']:
                                    print("⚠️ IA não retornou eventos válidos.")
                                    continue

                                # Corrige campos da IA (português para inglês)
                                for event in ai_data.get('events', []):
                                    # Mapeia campos de português para inglês
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
                                    corrected_event = {}
                                    for key, value in event.items():
                                        corrected_key = field_mapping.get(key, key)
                                        corrected_event[corrected_key] = value

                                    # Atualiza o evento com campos corrigidos
                                    event.clear()
                                    event.update(corrected_event)

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

                # Se não usou ferramenta, processa como conversa normal
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
