import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Any, Optional
from pathlib import Path

class DatabaseManager:
    def __init__(self, db_path: str = "memory.db"):
        self.db_path = db_path
        self.init_database()

    def init_database(self) -> None:
        """Inicializa o banco de dados com as tabelas necessárias"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Tabela de eventos
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                title TEXT NOT NULL,
                description TEXT,
                category TEXT NOT NULL,
                priority TEXT DEFAULT 'media',
                time TEXT,
                location TEXT,
                reminder TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Tabela de interações
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS interactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                human_message TEXT,
                assistant_message TEXT,
                context TEXT
            )
        ''')

        # Tabela de lembretes
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS reminders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_id INTEGER,
                reminder_time TIMESTAMP,
                message TEXT,
                is_sent BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (event_id) REFERENCES events (id)
            )
        ''')

        # Tabela de identidades/contexto
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS identities (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                role TEXT,
                relationship TEXT,
                preferences TEXT,
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        conn.commit()
        conn.close()

    def save_events(self, events_data: Dict[str, Any]) -> bool:
        """Salva eventos no banco de dados"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            date = events_data.get('date')
            events = events_data.get('events', [])

            for event in events:
                cursor.execute('''
                    INSERT INTO events (date, title, description, category, priority, time, location, reminder)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    date,
                    event.get('title', ''),
                    event.get('description', ''),
                    event.get('category', 'outros'),
                    event.get('priority', 'media'),
                    event.get('time'),
                    event.get('location'),
                    event.get('reminder')
                ))

            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Erro ao salvar eventos: {e}")
            return False

    def save_interaction(self, human_message: str, assistant_message: str, context: str = "") -> None:
        """Salva uma interação no banco de dados"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute('''
                INSERT INTO interactions (human_message, assistant_message, context)
                VALUES (?, ?, ?)
            ''', (human_message, assistant_message, context))

            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Erro ao salvar interação: {e}")

    def get_events_by_date(self, date: str) -> List[Dict[str, Any]]:
        """Busca eventos por data"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute('''
                SELECT * FROM events WHERE date = ? ORDER BY time ASC
            ''', (date,))

            events = []
            for row in cursor.fetchall():
                events.append({
                    'id': row[0],
                    'date': row[1],
                    'title': row[2],
                    'description': row[3],
                    'category': row[4],
                    'priority': row[5],
                    'time': row[6],
                    'location': row[7],
                    'reminder': row[8]
                })

            conn.close()
            return events
        except Exception as e:
            print(f"Erro ao buscar eventos: {e}")
            return []

    def get_recent_interactions(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Busca interações recentes"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute('''
                SELECT * FROM interactions ORDER BY timestamp DESC LIMIT ?
            ''', (limit,))

            interactions = []
            for row in cursor.fetchall():
                interactions.append({
                    'id': row[0],
                    'timestamp': row[1],
                    'human_message': row[2],
                    'assistant_message': row[3],
                    'context': row[4]
                })

            conn.close()
            return interactions
        except Exception as e:
            print(f"Erro ao buscar interações: {e}")
            return []

    def get_memory_context(self) -> Dict[str, Any]:
        """Retorna contexto completo da memória"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Busca eventos dos últimos 7 dias
            cursor.execute('''
                SELECT * FROM events
                WHERE date >= date('now', '-7 days')
                ORDER BY date DESC, time ASC
            ''')

            recent_events = []
            for row in cursor.fetchall():
                recent_events.append({
                    'id': row[0],
                    'date': row[1],
                    'title': row[2],
                    'description': row[3],
                    'category': row[4],
                    'priority': row[5],
                    'time': row[6],
                    'location': row[7],
                    'reminder': row[8]
                })

            # Busca interações recentes
            cursor.execute('''
                SELECT * FROM interactions
                ORDER BY timestamp DESC LIMIT 20
            ''')

            recent_interactions = []
            for row in cursor.fetchall():
                recent_interactions.append({
                    'id': row[0],
                    'timestamp': row[1],
                    'human_message': row[2],
                    'assistant_message': row[3],
                    'context': row[4]
                })

            conn.close()

            return {
                'events': recent_events,
                'interactions': recent_interactions
            }
        except Exception as e:
            print(f"Erro ao buscar contexto: {e}")
            return {'events': [], 'interactions': []}
