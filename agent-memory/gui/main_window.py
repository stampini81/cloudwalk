import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import queue
from datetime import datetime
from typing import Dict, Any, Optional
import json

class MemoryAssistantGUI:
    def __init__(self, db_manager, reminder_system):
        self.db_manager = db_manager
        self.reminder_system = reminder_system
        self.message_queue: queue.Queue = queue.Queue()

        self.root = tk.Tk()
        self.root.title("Assistente de Memória - IA")
        self.root.geometry("800x600")
        self.root.configure(bg='#f0f0f0')

        self.setup_ui()
        self.start_message_processor()

    def setup_ui(self) -> None:
        """Configura a interface do usuário"""
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky="nsew")

        # Configurar grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)

        # Título
        title_label = ttk.Label(main_frame, text="🎤 Assistente de Memória IA",
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))

        # Botões de controle
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=1, column=0, columnspan=3, pady=(0, 10))

        self.record_button = ttk.Button(button_frame, text="🎤 Gravar Áudio",
                                       command=self.start_recording)
        self.record_button.pack(side=tk.LEFT, padx=(0, 10))

        self.stop_button = ttk.Button(button_frame, text="⏹️ Parar",
                                     command=self.stop_recording, state='disabled')
        self.stop_button.pack(side=tk.LEFT, padx=(0, 10))

        self.clear_button = ttk.Button(button_frame, text="🗑️ Limpar",
                                      command=self.clear_chat)
        self.clear_button.pack(side=tk.LEFT)

        # Área de chat
        chat_frame = ttk.LabelFrame(main_frame, text="Conversa", padding="5")
        chat_frame.grid(row=2, column=0, columnspan=3, sticky="nsew")
        chat_frame.columnconfigure(0, weight=1)
        chat_frame.rowconfigure(0, weight=1)

        self.chat_area = scrolledtext.ScrolledText(chat_frame, wrap=tk.WORD,
                                                  height=20, width=80)
        self.chat_area.grid(row=0, column=0, sticky="nsew")

        # Área de eventos
        events_frame = ttk.LabelFrame(main_frame, text="📅 Eventos Recentes", padding="5")
        events_frame.grid(row=3, column=0, columnspan=3, sticky="ew", pady=(10, 0))
        events_frame.columnconfigure(0, weight=1)

        self.events_text = scrolledtext.ScrolledText(events_frame, wrap=tk.WORD,
                                                    height=8, width=80)
        self.events_text.grid(row=0, column=0, sticky="ew")

        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Pronto para gravar")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var,
                              relief=tk.SUNKEN, anchor=tk.W)
        status_bar.grid(row=4, column=0, columnspan=3, sticky="ew", pady=(10, 0))

        # Inicializar interface
        self.update_events_display()
        self.add_message("Sistema", "Assistente de memória iniciado! Diga 'sair' para encerrar.", "system")

    def start_recording(self) -> None:
        """Inicia gravação de áudio"""
        self.record_button.config(state='disabled')
        self.stop_button.config(state='normal')
        self.status_var.set("🎤 Gravando... Pressione 'Parar' para finalizar")

        # Inicia gravação em thread separada
        self.recording_thread = threading.Thread(target=self.record_audio_thread)
        self.recording_thread.daemon = True
        self.recording_thread.start()

    def stop_recording(self) -> None:
        """Para gravação de áudio"""
        self.record_button.config(state='normal')
        self.stop_button.config(state='disabled')
        self.status_var.set("Processando áudio...")

        # Sinaliza para parar gravação
        self.stop_recording_flag = True

    def record_audio_thread(self) -> None:
        """Thread para gravação de áudio"""
        try:
            from utils.record_audio import record_audio

            # Simula gravação (você precisará adaptar para sua função real)
            import time
            time.sleep(2)  # Simula tempo de gravação

            # Processa áudio
            self.process_audio("Áudio gravado com sucesso!")

        except Exception as e:
            self.add_message("Erro", f"Erro na gravação: {e}", "error")
        finally:
            self.root.after(0, self.reset_recording_ui)

    def reset_recording_ui(self) -> None:
        """Reseta interface de gravação"""
        self.record_button.config(state='normal')
        self.stop_button.config(state='disabled')
        self.status_var.set("Pronto para gravar")

    def process_audio(self, audio_text: str) -> None:
        """Processa áudio gravado"""
        self.add_message("Você", audio_text, "user")

        # Simula processamento com IA
        response = f"Processei seu áudio: '{audio_text}'. Eventos categorizados e salvos!"
        self.add_message("Assistente", response, "assistant")

        # Atualiza eventos
        self.update_events_display()

    def add_message(self, sender: str, message: str, msg_type: str = "normal") -> None:
        """Adiciona mensagem à área de chat"""
        timestamp = datetime.now().strftime("%H:%M:%S")

        # Configura cores baseadas no tipo
        if msg_type == "user":
            prefix = "👤"
            color = "blue"
        elif msg_type == "assistant":
            prefix = "🤖"
            color = "green"
        elif msg_type == "system":
            prefix = "⚙️"
            color = "gray"
        elif msg_type == "error":
            prefix = "❌"
            color = "red"
        else:
            prefix = "💬"
            color = "black"

        formatted_message = f"[{timestamp}] {prefix} {sender}: {message}\n"

        # Adiciona à fila para processamento na thread principal
        self.message_queue.put((formatted_message, color))

    def start_message_processor(self) -> None:
        """Inicia processador de mensagens"""
        self.process_messages()

    def process_messages(self) -> None:
        """Processa mensagens da fila"""
        try:
            while True:
                message, color = self.message_queue.get_nowait()

                # Adiciona mensagem ao chat
                self.chat_area.insert(tk.END, message)
                self.chat_area.see(tk.END)

                # Aplica cor (simplificado)
                if color != "black":
                    # Marca para aplicar cor
                    pass

        except queue.Empty:
            pass

        # Agenda próximo processamento
        self.root.after(100, self.process_messages)

    def update_events_display(self) -> None:
        """Atualiza display de eventos"""
        try:
            # Busca eventos recentes do banco
            today = datetime.now().strftime("%d/%m/%Y")
            events = self.db_manager.get_events_by_date(today)

            # Limpa área de eventos
            self.events_text.delete(1.0, tk.END)

            if events:
                self.events_text.insert(tk.END, f"📅 Eventos de hoje ({today}):\n\n")

                for event in events:
                    category_emoji = self.get_category_emoji(event['category'])
                    priority_emoji = self.get_priority_emoji(event['priority'])

                    event_text = f"{category_emoji} {priority_emoji} {event['title']}\n"
                    if event['time']:
                        event_text += f"   ⏰ {event['time']}\n"
                    if event['location']:
                        event_text += f"   📍 {event['location']}\n"
                    if event['description']:
                        event_text += f"   📝 {event['description']}\n"
                    event_text += "\n"

                    self.events_text.insert(tk.END, event_text)
            else:
                self.events_text.insert(tk.END, "Nenhum evento registrado para hoje.")

        except Exception as e:
            self.events_text.insert(tk.END, f"Erro ao carregar eventos: {e}")

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

    def clear_chat(self) -> None:
        """Limpa área de chat"""
        self.chat_area.delete(1.0, tk.END)
        self.add_message("Sistema", "Chat limpo!", "system")

    def run(self) -> None:
        """Executa a interface gráfica"""
        # Inicia sistema de lembretes
        self.reminder_system.start()

        # Executa interface
        self.root.mainloop()

        # Para sistema de lembretes ao sair
        self.reminder_system.stop()
