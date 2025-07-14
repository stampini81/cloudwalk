import mysql.connector
from mysql.connector import Error
from typing import Dict, List, Any, Optional, cast
from datetime import datetime
import re

class IdentityManager:
    def __init__(self, host="localhost", user="root", password="", database="agent_memory"):
        self.connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.init_identity_table()

    def init_identity_table(self) -> None:
        try:
            cursor = self.connection.cursor()
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
        except Error as e:
            print(f"Erro ao inicializar tabela de identidades: {e}")

    def add_identity(self, name: str, role: Optional[str] = None, relationship: Optional[str] = None,
                    preferences: Optional[str] = None, notes: Optional[str] = None) -> bool:
        try:
            cursor = self.connection.cursor()
            cursor.execute('''
                INSERT INTO identities (name, role, relationship, preferences, notes)
                VALUES (%s, %s, %s, %s, %s)
            ''', (name, role, relationship, preferences, notes))
            self.connection.commit()
            print(f"✅ Identidade '{name}' adicionada com sucesso!")
            return True
        except Error as e:
            print(f"Erro ao adicionar identidade: {e}")
            return False

    def get_identity(self, name: str) -> Optional[Dict[str, Any]]:
        try:
            cursor = self.connection.cursor()
            cursor.execute('''
                SELECT * FROM identities WHERE name = %s
            ''', (name,))
            row = cursor.fetchone()
            if row:
                row_data = cast(Any, row)
                return {
                    'id': row_data[0],
                    'name': row_data[1],
                    'role': row_data[2],
                    'relationship': row_data[3],
                    'preferences': row_data[4],
                    'notes': row_data[5],
                    'created_at': row_data[6],
                    'updated_at': row_data[7]
                }
            return None
        except Error as e:
            print(f"Erro ao buscar identidade: {e}")
            return None

    def update_identity(self, name: str, **kwargs: Any) -> bool:
        try:
            cursor = self.connection.cursor()
            update_fields = []
            values = []
            for field, value in kwargs.items():
                if field in ['role', 'relationship', 'preferences', 'notes']:
                    update_fields.append(f"{field} = %s")
                    values.append(value)
            if update_fields:
                values.append(datetime.now())
                values.append(name)
                query = f'''
                    UPDATE identities
                    SET {', '.join(update_fields)}, updated_at = %s
                    WHERE name = %s
                '''
                cursor.execute(query, values)
                self.connection.commit()
                print(f"✅ Identidade '{name}' atualizada!")
                return True
            return False
        except Error as e:
            print(f"Erro ao atualizar identidade: {e}")
            return False

    def get_all_identities(self) -> List[Dict[str, Any]]:
        try:
            cursor = self.connection.cursor()
            cursor.execute('''
                SELECT * FROM identities ORDER BY name
            ''')
            identities = []
            for row in cursor.fetchall():
                row_data = cast(Any, row)
                identities.append({
                    'id': row_data[0],
                    'name': row_data[1],
                    'role': row_data[2],
                    'relationship': row_data[3],
                    'preferences': row_data[4],
                    'notes': row_data[5],
                    'created_at': row_data[6],
                    'updated_at': row_data[7]
                })
            return identities
        except Error as e:
            print(f"Erro ao buscar identidades: {e}")
            return []

    def extract_identities_from_text(self, text: str) -> List[Dict[str, Any]]:
        """Extrai informações de identidade do texto"""
        identities = []
        try:
            # Padrões para reconhecer pessoas
            patterns = [
                r'(?:meu|minha)\s+(?:amigo|amiga|irmão|irmã|pai|mãe|filho|filha|marido|esposa|namorado|namorada|colega|vizinho|professor|médico)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)',
                r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+(?:é|é meu|é minha)\s+(amigo|amiga|irmão|irmã|pai|mãe|filho|filha|marido|esposa|namorado|namorada)',
                r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+(?:trabalha|estuda|mora|gosta|prefere|está|foi|vai)\s+',
                r'(?:conheci|encontrei|falei com|visitei|chamei)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)',
                r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+(?:disse|falou|mencionou|contou|explicou)',
                r'(?:reunião|almoço|jantar|encontro|conversa)\s+(?:com|entre)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)'
            ]

            for pattern in patterns:
                matches = re.findall(pattern, text)
                for match in matches:
                    if isinstance(match, tuple):
                        name = match[0]
                        relationship = match[1] if len(match) > 1 else None
                    else:
                        name = match
                        relationship = None

                    # Verifica se já existe
                    existing = self.get_identity(name)
                    if not existing:
                        # Adiciona nova identidade
                        self.add_identity(name, relationship=relationship)
                        identities.append({
                            'name': name,
                            'relationship': relationship,
                            'action': 'added'
                        })
                    else:
                        identities.append({
                            'name': name,
                            'relationship': existing.get('relationship'),
                            'action': 'found'
                        })

            return identities
        except Exception as e:
            print(f"Erro ao extrair identidades: {e}")
            return []

    def _is_valid_person_name(self, name: str) -> bool:
        """Verifica se o nome é válido para uma pessoa"""
        # Remove palavras que não são nomes de pessoas
        invalid_words = ['hoje', 'amanhã', 'ontem', 'agora', 'depois', 'antes', 'sempre', 'nunca']
        return name.lower() not in invalid_words and len(name) > 1

    def get_context_for_identity(self, name: str) -> str:
        """Retorna contexto para uma identidade específica"""
        try:
            identity = self.get_identity(name)
            if identity:
                context = f"Pessoa: {identity['name']}"
                if identity.get('role'):
                    context += f", Papel: {identity['role']}"
                if identity.get('relationship'):
                    context += f", Relacionamento: {identity['relationship']}"
                if identity.get('preferences'):
                    context += f", Preferências: {identity['preferences']}"
                if identity.get('notes'):
                    context += f", Notas: {identity['notes']}"
                return context
            return ""
        except Exception as e:
            print(f"Erro ao buscar contexto da identidade: {e}")
            return ""

    def get_all_contexts(self) -> str:
        """Retorna contexto de todas as identidades"""
        try:
            identities = self.get_all_identities()
            if not identities:
                return ""

            contexts = []
            for identity in identities:
                context = self.get_context_for_identity(identity['name'])
                if context:
                    contexts.append(context)

            return "\n".join(contexts)
        except Exception as e:
            print(f"Erro ao buscar todos os contextos: {e}")
            return ""
