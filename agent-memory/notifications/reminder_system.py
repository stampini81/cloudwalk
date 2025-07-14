import threading
import time
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import mysql.connector
from mysql.connector import Error
import json

# Try to import plyer, but don't fail if not available
try:
    from plyer import notification  # type: ignore
    PLYER_AVAILABLE = True
except ImportError:
    PLYER_AVAILABLE = False
    print("⚠️ Plyer não disponível - notificações desabilitadas")

class ReminderSystem:
    def __init__(self, host="localhost", user="root", password="", database="agent_memory"):
        self.connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.running = False
        self.reminder_thread: Optional[threading.Thread] = None

    def start(self) -> None:
        if not self.running:
            self.running = True
            self.reminder_thread = threading.Thread(target=self._check_reminders, daemon=True)
            self.reminder_thread.start()
            print("🔔 Sistema de lembretes iniciado!")

    def stop(self) -> None:
        self.running = False
        if self.reminder_thread:
            self.reminder_thread.join()
        print("🔔 Sistema de lembretes parado!")

    def _check_reminders(self) -> None:
        while self.running:
            try:
                self._process_reminders()
                time.sleep(60)
            except Exception as e:
                print(f"Erro no sistema de lembretes: {e}")
                time.sleep(60)

    def _process_reminders(self) -> None:
        try:
            cursor = self.connection.cursor()
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute('''
                SELECT r.id, r.event_id, r.reminder_time, r.message, r.is_sent, e.title, e.date, e.time
                FROM reminders r
                JOIN events e ON r.event_id = e.id
                WHERE r.is_sent = 0 AND r.reminder_time <= %s
            ''', (now,))
            reminders = cursor.fetchall()
            for reminder in reminders:
                reminder_id, event_id, reminder_time, message, is_sent, event_title, event_date, event_time = reminder
                if PLYER_AVAILABLE:
                    self._send_notification(event_title, message, event_time, event_date)
                # Marca como enviado
                cursor.execute('UPDATE reminders SET is_sent = 1 WHERE id = %s', (str(reminder_id),))
            self.connection.commit()
        except Error as e:
            print(f"Erro ao processar lembretes: {e}")

    def _send_notification(self, title, message, event_time, event_date):
        if PLYER_AVAILABLE:
            try:
                # Verifica se notification está disponível de forma mais robusta
                import sys
                notification_module = sys.modules.get('plyer.notification')
                if notification_module and hasattr(notification_module, 'notify'):
                    notification_module.notify(
                        title=f"🔔 {title}",
                        message=f"{message}\nData: {event_date} {event_time if event_time else ''}",
                        timeout=10
                    )
                else:
                    print(f"🔔 Lembrete: {title} - {message}")
            except Exception as e:
                print(f"Erro ao enviar notificação: {e}")
                print(f"🔔 Lembrete: {title} - {message}")
        else:
            print(f"🔔 Lembrete: {title} - {message}")

    def create_reminder(self, event_id: int, reminder_time: str, message: str) -> None:
        try:
            cursor = self.connection.cursor()
            cursor.execute('''
                INSERT INTO reminders (event_id, reminder_time, message, is_sent)
                VALUES (%s, %s, %s, 0)
            ''', (event_id, reminder_time, message))
            self.connection.commit()
        except Error as e:
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
