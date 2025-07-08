import threading
import time
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import sqlite3
import json

# Try to import plyer, but don't fail if not available
try:
    from plyer import notification  # type: ignore
    PLYER_AVAILABLE = True
except ImportError:
    PLYER_AVAILABLE = False
    print("⚠️ Plyer não disponível - notificações desabilitadas")

class ReminderSystem:
    def __init__(self, db_path: str = "memory.db"):
        self.db_path = db_path
        self.running = False
        self.reminder_thread: Optional[threading.Thread] = None

    def start(self) -> None:
        """Inicia o sistema de lembretes em background"""
        if not self.running:
            self.running = True
            self.reminder_thread = threading.Thread(target=self._check_reminders, daemon=True)
            self.reminder_thread.start()
            print("🔔 Sistema de lembretes iniciado!")

    def stop(self) -> None:
        """Para o sistema de lembretes"""
        self.running = False
        if self.reminder_thread:
            self.reminder_thread.join()
        print("🔔 Sistema de lembretes parado!")

    def _check_reminders(self) -> None:
        """Verifica lembretes em background"""
        while self.running:
            try:
                self._process_reminders()
                time.sleep(60)  # Verifica a cada minuto
            except Exception as e:
                print(f"Erro no sistema de lembretes: {e}")
                time.sleep(60)

    def _process_reminders(self) -> None:
        """Processa lembretes pendentes"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Busca lembretes que devem ser enviados
            cursor.execute('''
                SELECT r.id, r.message, e.title, e.time, e.date
                FROM reminders r
                JOIN events e ON r.event_id = e.id
                WHERE r.is_sent = FALSE AND r.reminder_time <= datetime('now')
            ''')

            reminders = cursor.fetchall()

            for reminder in reminders:
                reminder_id, message, title, event_time, event_date = reminder

                # Envia notificação
                self._send_notification(title, message, event_time, event_date)

                # Marca como enviado
                cursor.execute('''
                    UPDATE reminders SET is_sent = TRUE WHERE id = ?
                ''', (reminder_id,))

            conn.commit()
            conn.close()

        except Exception as e:
            print(f"Erro ao processar lembretes: {e}")

    def _send_notification(self, title: str, message: str, event_time: Optional[str], event_date: str) -> None:
        """Envia notificação do sistema"""
        try:
            if not PLYER_AVAILABLE:
                print(f"🔔 Lembrete: {title} - {message}")
                return

            notification_title = f"🔔 Lembrete: {title}"
            notification_message = f"{message}\nData: {event_date}"
            if event_time:
                notification_message += f"\nHorário: {event_time}"

            notification.notify(
                title=notification_title,
                message=notification_message,
                app_icon=None,  # e.g. 'C:\\icon_32x32.ico'
                timeout=10,  # seconds
            )

            print(f"🔔 Notificação enviada: {title}")

        except Exception as e:
            print(f"Erro ao enviar notificação: {e}")

    def create_reminder(self, event_id: int, reminder_time: str, message: str) -> None:
        """Cria um novo lembrete"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute('''
                INSERT INTO reminders (event_id, reminder_time, message)
                VALUES (?, ?, ?)
            ''', (event_id, reminder_time, message))

            conn.commit()
            conn.close()
            print(f"🔔 Lembrete criado para evento {event_id}")

        except Exception as e:
            print(f"Erro ao criar lembrete: {e}")

    def parse_reminder_time(self, reminder_text: str, event_date: str, event_time: Optional[str] = None) -> str:
        """Converte texto de lembrete em timestamp"""
        try:
            # Converte data do evento
            event_datetime = datetime.strptime(event_date, "%d/%m/%Y")
            if event_time:
                event_datetime = datetime.strptime(f"{event_date} {event_time}", "%d/%m/%Y %H:%M")

            # Processa diferentes formatos de lembrete
            reminder_text = reminder_text.lower().strip()

            if "30min" in reminder_text or "30 minutos" in reminder_text:
                reminder_datetime = event_datetime - timedelta(minutes=30)
            elif "1h" in reminder_text or "1 hora" in reminder_text:
                reminder_datetime = event_datetime - timedelta(hours=1)
            elif "2h" in reminder_text or "2 horas" in reminder_text:
                reminder_datetime = event_datetime - timedelta(hours=2)
            elif "1 dia" in reminder_text or "1d" in reminder_text:
                reminder_datetime = event_datetime - timedelta(days=1)
            else:
                # Padrão: 1 hora antes
                reminder_datetime = event_datetime - timedelta(hours=1)

            return reminder_datetime.strftime("%Y-%m-%d %H:%M:%S")

        except Exception as e:
            print(f"Erro ao processar tempo do lembrete: {e}")
            # Retorna 1 hora antes como padrão
            event_datetime = datetime.strptime(event_date, "%d/%m/%Y")
            return (event_datetime - timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S")
