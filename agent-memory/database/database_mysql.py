import mysql.connector
from mysql.connector import Error
from typing import List, Dict, Any, Optional, cast

class DatabaseManager:
    def __init__(self, host="localhost", user="root", password="", database="agent_memory"):
        self.connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.init_database()

    def init_database(self) -> None:
        cursor = self.connection.cursor()
        # Tabela de eventos
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS events (
                id INT AUTO_INCREMENT PRIMARY KEY,
                date VARCHAR(20) NOT NULL,
                title VARCHAR(255) NOT NULL,
                description TEXT,
                category VARCHAR(50) NOT NULL,
                priority VARCHAR(20) DEFAULT 'media',
                time VARCHAR(10),
                location VARCHAR(255),
                reminder VARCHAR(255),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            )
        ''')
        # Tabela de interações
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS interactions (
                id INT AUTO_INCREMENT PRIMARY KEY,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                human_message TEXT,
                assistant_message TEXT,
                context TEXT
            )
        ''')
        # Tabela de lembretes
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS reminders (
                id INT AUTO_INCREMENT PRIMARY KEY,
                event_id INT,
                reminder_time TIMESTAMP,
                message VARCHAR(255),
                is_sent TINYINT(1) DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (event_id) REFERENCES events(id)
            )
        ''')
        # Tabela de identidades
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS identities (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                role VARCHAR(100),
                relationship VARCHAR(100),
                preferences TEXT,
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            )
        ''')
        self.connection.commit()

    def save_events(self, events_data: Dict[str, Any]) -> bool:
        try:
            cursor = self.connection.cursor()
            date = events_data.get('date')
            events = events_data.get('events', [])
            for event in events:
                cursor.execute('''
                    INSERT INTO events (date, title, description, category, priority, time, location, reminder)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
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
            self.connection.commit()
            return True
        except Error as e:
            print(f"Erro ao salvar eventos: {e}")
            return False

    def save_interaction(self, human_message: str, assistant_message: str, context: str = "") -> None:
        try:
            cursor = self.connection.cursor()
            cursor.execute('''
                INSERT INTO interactions (human_message, assistant_message, context)
                VALUES (%s, %s, %s)
            ''', (human_message, assistant_message, context))
            self.connection.commit()
        except Error as e:
            print(f"Erro ao salvar interação: {e}")

    def get_events_by_date(self, date: str) -> List[Dict[str, Any]]:
        try:
            cursor = self.connection.cursor()
            cursor.execute('''
                SELECT * FROM events WHERE date = %s ORDER BY time ASC
            ''', (date,))
            events = []
            for row in cursor.fetchall():
                row_data = cast(Any, row)
                events.append({
                    'id': row_data[0],
                    'date': row_data[1],
                    'title': row_data[2],
                    'description': row_data[3],
                    'category': row_data[4],
                    'priority': row_data[5],
                    'time': row_data[6],
                    'location': row_data[7],
                    'reminder': row_data[8],
                    'created_at': row_data[9],
                    'updated_at': row_data[10]
                })
            return events
        except Error as e:
            print(f"Erro ao buscar eventos: {e}")
            return []

    def get_recent_interactions(self, limit: int = 10) -> List[Dict[str, Any]]:
        try:
            cursor = self.connection.cursor()
            cursor.execute('''
                SELECT * FROM interactions ORDER BY timestamp DESC LIMIT %s
            ''', (limit,))
            interactions = []
            for row in cursor.fetchall():
                row_data = cast(Any, row)
                interactions.append({
                    'id': row_data[0],
                    'timestamp': row_data[1],
                    'human_message': row_data[2],
                    'assistant_message': row_data[3],
                    'context': row_data[4]
                })
            return interactions
        except Error as e:
            print(f"Erro ao buscar interações: {e}")
            return []

    def get_memory_context(self) -> Dict[str, Any]:
        try:
            cursor = self.connection.cursor()
            # Busca eventos dos últimos 7 dias
            cursor.execute('''
                SELECT * FROM events
                WHERE date >= DATE_SUB(CURDATE(), INTERVAL 7 DAY)
                ORDER BY date DESC, time ASC
            ''')
            recent_events = []
            for row in cursor.fetchall():
                row_data = cast(Any, row)
                recent_events.append({
                    'id': row_data[0],
                    'date': row_data[1],
                    'title': row_data[2],
                    'description': row_data[3],
                    'category': row_data[4],
                    'priority': row_data[5],
                    'time': row_data[6],
                    'location': row_data[7],
                    'reminder': row_data[8],
                    'created_at': row_data[9],
                    'updated_at': row_data[10]
                })
            # Busca interações recentes
            cursor.execute('''
                SELECT * FROM interactions ORDER BY timestamp DESC LIMIT 20
            ''')
            recent_interactions = []
            for row in cursor.fetchall():
                row_data = cast(Any, row)
                recent_interactions.append({
                    'id': row_data[0],
                    'timestamp': row_data[1],
                    'human_message': row_data[2],
                    'assistant_message': row_data[3],
                    'context': row_data[4]
                })
            return {
                'events': recent_events,
                'interactions': recent_interactions
            }
        except Error as e:
            print(f"Erro ao buscar contexto: {e}")
            return {'events': [], 'interactions': []}
