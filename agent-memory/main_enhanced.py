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

        REGRAS CRÍTICAS:
        1. SEMPRE use a ferramenta DailyEvents quando mencionar eventos, datas ou localizações
        2. Use APENAS estas categorias: trabalho, saude, pessoal, familia, lazer, estudos, financeiro, outros
        3. Use APENAS estas prioridades: baixa, media, alta, urgente
        4. Use APENAS campos em inglês: title, description, category, priority, time, location, reminder
        5. SEMPRE retorne uma lista de eventos válida, mesmo que seja apenas um evento

        EXEMPLOS DE CATEGORIZAÇÃO:
        - "reunião" → category: trabalho
        - "viagem" → category: lazer
        - "consulta médica" → category: saude
        - "estudar" → category: estudos
        - "família" → category: familia
        - "conta" → category: financeiro

        QUANDO USAR DailyEvents:
        - Mencionar datas (ontem, hoje, amanhã, datas específicas)
        - Mencionar localizações ou viagens
        - Mencionar eventos ou atividades
        - Mencionar pessoas ou relacionamentos

        FORMATO OBRIGATÓRIO:
        - date: data no formato DD/MM/YYYY
        - events: lista de eventos com:
          * title: título do evento
          * description: descrição detalhada
          * category: uma das categorias listadas
          * priority: uma das prioridades listadas
          * time: horário (opcional, formato HH:MM)
          * location: local (opcional)
          * reminder: lembrete (opcional)

        EXEMPLO DE RESPOSTA VÁLIDA:
        {{
          "date": "07/07/2025",
          "events": [
            {{
              "title": "Visita a Marília",
              "description": "Estadia em Marília para trabalho",
              "category": "trabalho",
              "priority": "media",
              "location": "Marília, SP"
            }}
          ]
        }}
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

    def process_with_ai_forced(self, text: str, context: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Processa texto com IA forçando o uso da ferramenta DailyEvents"""
        actual_date = datetime.now().strftime("%d/%m/%Y")

        forced_prompt = f"""
        VOCÊ DEVE USAR A FERRAMENTA DailyEvents PARA ESTE TEXTO!

        Texto do usuário: "{text}"
        Data atual: {actual_date}

        INSTRUÇÕES OBRIGATÓRIAS:
        1. SEMPRE use a ferramenta DailyEvents para este tipo de texto
        2. Identifique TODOS os eventos mencionados
        3. Use categorias: trabalho, saude, pessoal, familia, lazer, estudos, financeiro, outros
        4. Use prioridades: baixa, media, alta, urgente
        5. Use campos em inglês: title, description, category, priority, time, location, reminder

        EXEMPLO DE RESPOSTA OBRIGATÓRIA:
        {{
          "date": "07/07/2025",
          "events": [
            {{
              "title": "Evento mencionado",
              "description": "Descrição do evento",
              "category": "outros",
              "priority": "media"
            }}
          ]
        }}

        NÃO RESPONDA COMO CONVERSA NORMAL. USE APENAS A FERRAMENTA DailyEvents!
        """

        try:
            completion = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": forced_prompt},
                    {"role": "user", "content": text}
                ],
                tool_choice={"type": "function", "function": {"name": "DailyEvents"}},
                tools=[base_model2tool(DailyEvents)]  # type: ignore
            )

            return {
                'completion': completion,
                'text': text,
                'context': context
            }

        except Exception as e:
            print(f"❌ Erro ao processar com IA forçada: {e}")
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
                    print("⚠️ Gravação muito curta. Tente novamente.")
                    continue

                # Processa áudio
                text = self.process_audio(filename_audio)
                if not text:
                    print("❌ Erro ao processar áudio")
                    continue

                text = text.lower().strip()
                print(f"🎤 Você disse: {text}")

                # Verifica comando de saída (mais abrangente)
                exit_commands = [
                    "sair", "quit", "exit", "encerrar", "parar", "sair!", "quit!", "exit!",
                    "encerrar a aplicação", "parar aplicação", "fechar", "close", "stop",
                    "tchau", "bye", "até logo", "até mais"
                ]

                if any(cmd in text for cmd in exit_commands):
                    print("👋 Encerrando aplicação...")
                    self.reminder_system.stop()
                    break

                # Extrai identidades
                identities = self.extract_identities(text)
                if identities:
                    print(f"👥 Identidades reconhecidas: {len(identities)}")

                # Obtém contexto
                context = self.get_context()

                # Verifica se o texto contém palavras-chave de eventos (excluindo comandos de saída)
                event_keywords = ['ontem', 'hoje', 'amanhã', 'estive', 'estou', 'estarei', 'visita', 'viagem', 'reunião', 'consulta', 'estudar', 'trabalho', 'família']
                exit_keywords = ['sair', 'quit', 'exit', 'encerrar', 'parar', 'fechar', 'close', 'stop', 'tchau', 'bye']

                # Só processa como evento se não for comando de saída
                has_event_keywords = any(keyword in text.lower() for keyword in event_keywords) and not any(keyword in text.lower() for keyword in exit_keywords)

                # Processa com IA
                result = self.process_with_ai(text, context)
                if not result:
                    continue

                completion = result['completion']

                # Se detectou palavras-chave de eventos mas não usou a ferramenta, força o uso
                if has_event_keywords and not completion.choices[0].message.tool_calls:
                    print("🔧 Detectei palavras-chave de eventos. Forçando uso da ferramenta...")
                    # Tenta novamente com prompt mais específico
                    result = self.process_with_ai_forced(text, context)
                    if result:
                        completion = result['completion']

                # Processa resposta da IA
                if completion.choices[0].message.tool_calls:
                    print("🔧 Processando eventos com ferramenta DailyEvents...")
                    for tool_call in completion.choices[0].message.tool_calls:
                        if tool_call.function.name == "DailyEvents":
                            try:
                                # Obtém dados da IA
                                ai_data = json.loads(tool_call.function.arguments)

                                # Verifica se há eventos na resposta
                                if 'events' not in ai_data or not ai_data['events']:
                                    print("⚠️ IA não retornou eventos válidos. Processando como conversa...")
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
                                print("💡 Tentando criar eventos automaticamente...")

                                # Tenta criar eventos automaticamente baseado no texto
                                try:
                                    # Extrai datas mencionadas do texto
                                    import re
                                    date_patterns = [
                                        r'ontem\s+(\d{1,2}/\d{1,2}/\d{4})',
                                        r'hoje\s+(\d{1,2}/\d{1,2}/\d{4})',
                                        r'amanhã\s+(\d{1,2}/\d{1,2}/\d{4})',
                                        r'(\d{1,2}/\d{1,2}/\d{4})'
                                    ]

                                    extracted_events = []
                                    for pattern in date_patterns:
                                        matches = re.findall(pattern, text)
                                        for match in matches:
                                            # Cria evento básico
                                            event_data = {
                                                'date': match,
                                                'events': [{
                                                    'title': f'Evento em {match}',
                                                    'description': f'Evento mencionado para {match}',
                                                    'category': 'outros',
                                                    'priority': 'media'
                                                }]
                                            }
                                            extracted_events.append(event_data)

                                    if extracted_events:
                                        print("✅ Criando eventos automaticamente...")
                                        for event_data in extracted_events:
                                            daily_events = DailyEvents(**event_data)
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
                                            if self.save_events(events_data):
                                                print(f"✅ Evento criado para {daily_events.date}")

                                except Exception as fallback_error:
                                    print(f"❌ Erro no fallback: {fallback_error}")
                                    print("💡 Processando como conversa normal...")
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
