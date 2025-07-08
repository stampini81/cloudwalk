import sqlite3
import json
from typing import Dict, List, Any, Optional
from datetime import datetime
import re

class IdentityManager:
    def __init__(self, db_path: str = "memory.db"):
        self.db_path = db_path
        self.init_identity_table()

    def init_identity_table(self) -> None:
        """Inicializa tabela de identidades se não existir"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

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
        except Exception as e:
            print(f"Erro ao inicializar tabela de identidades: {e}")

    def add_identity(self, name: str, role: Optional[str] = None, relationship: Optional[str] = None,
                    preferences: Optional[str] = None, notes: Optional[str] = None) -> bool:
        """Adiciona uma nova identidade"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute('''
                INSERT INTO identities (name, role, relationship, preferences, notes)
                VALUES (?, ?, ?, ?, ?)
            ''', (name, role, relationship, preferences, notes))

            conn.commit()
            conn.close()
            print(f"✅ Identidade '{name}' adicionada com sucesso!")
            return True
        except Exception as e:
            print(f"Erro ao adicionar identidade: {e}")
            return False

    def get_identity(self, name: str) -> Optional[Dict[str, Any]]:
        """Busca uma identidade por nome"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute('''
                SELECT * FROM identities WHERE name = ?
            ''', (name,))

            row = cursor.fetchone()
            conn.close()

            if row:
                return {
                    'id': row[0],
                    'name': row[1],
                    'role': row[2],
                    'relationship': row[3],
                    'preferences': row[4],
                    'notes': row[5],
                    'created_at': row[6],
                    'updated_at': row[7]
                }
            return None
        except Exception as e:
            print(f"Erro ao buscar identidade: {e}")
            return None

    def update_identity(self, name: str, **kwargs: Any) -> bool:
        """Atualiza uma identidade existente"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Constrói query de atualização dinamicamente
            update_fields = []
            values = []

            for field, value in kwargs.items():
                if field in ['role', 'relationship', 'preferences', 'notes']:
                    update_fields.append(f"{field} = ?")
                    values.append(value)

            if update_fields:
                values.append(datetime.now())
                values.append(name)

                query = f'''
                    UPDATE identities
                    SET {', '.join(update_fields)}, updated_at = ?
                    WHERE name = ?
                '''

                cursor.execute(query, values)
                conn.commit()
                conn.close()
                print(f"✅ Identidade '{name}' atualizada!")
                return True

            return False
        except Exception as e:
            print(f"Erro ao atualizar identidade: {e}")
            return False

    def get_all_identities(self) -> List[Dict[str, Any]]:
        """Retorna todas as identidades"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute('''
                SELECT * FROM identities ORDER BY name
            ''')

            identities = []
            for row in cursor.fetchall():
                identities.append({
                    'id': row[0],
                    'name': row[1],
                    'role': row[2],
                    'relationship': row[3],
                    'preferences': row[4],
                    'notes': row[5],
                    'created_at': row[6],
                    'updated_at': row[7]
                })

            conn.close()
            return identities
        except Exception as e:
            print(f"Erro ao buscar identidades: {e}")
            return []

    def extract_identities_from_text(self, text: str) -> List[Dict[str, Any]]:
        """Extrai informações de identidade do texto"""
        identities = []

        # Padrões para reconhecer pessoas (melhorados)
        patterns = [
            # Padrão: "meu amigo João", "minha irmã Maria"
            r'(?:meu|minha)\s+(?:amigo|amiga|irmão|irmã|pai|mãe|filho|filha|marido|esposa|namorado|namorada|colega|vizinho|professor|médico)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)',

            # Padrão: "João é meu amigo", "Maria é minha irmã"
            r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+(?:é|é meu|é minha)\s+(amigo|amiga|irmão|irmã|pai|mãe|filho|filha|marido|esposa|namorado|namorada)',

            # Padrão: "João trabalha", "Maria estuda" (mais específico)
            r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+(?:trabalha|estuda|mora|gosta|prefere|está|foi|vai)\s+',

            # Padrão: "conheci João", "encontrei Maria"
            r'(?:conheci|encontrei|falei com|visitei|chamei)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)',

            # Padrão: "João disse", "Maria falou"
            r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+(?:disse|falou|mencionou|contou|explicou)',

            # Padrão: "reunião com João", "almoço com Maria"
            r'(?:reunião|almoço|jantar|encontro|conversa)\s+(?:com|entre)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)'
        ]

        for pattern in patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                name = match.group(1).strip()
                relationship = match.group(2) if len(match.groups()) > 1 else None

                # Filtra palavras que não são nomes de pessoas
                if self._is_valid_person_name(name):
                    # Verifica se já existe
                    existing = self.get_identity(name)
                    if not existing:
                        # Adiciona nova identidade
                        self.add_identity(name, relationship=relationship)
                        identities.append({
                            'name': name,
                            'relationship': relationship,
                            'new': True
                        })
                    else:
                        identities.append(existing)

        return identities

    def _is_valid_person_name(self, name: str) -> bool:
        """Verifica se o nome é válido (não é verbo ou palavra comum)"""
        # Lista de palavras que não são nomes de pessoas
        invalid_words = {
            'estive', 'estava', 'estou', 'está', 'estão', 'estamos',
            'fui', 'foi', 'vou', 'vai', 'vão', 'vamos',
            'tenho', 'tem', 'temos', 'têm',
            'quero', 'quer', 'queremos', 'querem',
            'posso', 'pode', 'podemos', 'podem',
            'devo', 'deve', 'devemos', 'devem',
            'preciso', 'precisa', 'precisamos', 'precisam',
            'ontem', 'hoje', 'amanhã', 'agora', 'depois',
            'aqui', 'ali', 'lá', 'cá', 'onde',
            'como', 'quando', 'porque', 'por que',
            'trabalho', 'trabalha', 'trabalhando',
            'estudo', 'estuda', 'estudando',
            'moro', 'mora', 'morando',
            'gosto', 'gosta', 'gostando'
        }

        # Verifica se a palavra está na lista de inválidas
        name_lower = name.lower().strip()
        if name_lower in invalid_words:
            return False

        # Verifica se tem pelo menos 2 caracteres
        if len(name_lower) < 2:
            return False

        # Verifica se começa com letra maiúscula
        if not name[0].isupper():
            return False

        return True

    def get_context_for_identity(self, name: str) -> str:
        """Retorna contexto para uma identidade específica"""
        identity = self.get_identity(name)
        if not identity:
            return ""

        context = f"Pessoa: {identity['name']}"
        if identity['role']:
            context += f"\nFunção: {identity['role']}"
        if identity['relationship']:
            context += f"\nRelacionamento: {identity['relationship']}"
        if identity['preferences']:
            context += f"\nPreferências: {identity['preferences']}"
        if identity['notes']:
            context += f"\nNotas: {identity['notes']}"

        return context

    def get_all_contexts(self) -> str:
        """Retorna contexto de todas as identidades"""
        identities = self.get_all_identities()
        if not identities:
            return ""

        contexts = []
        for identity in identities:
            context = self.get_context_for_identity(identity['name'])
            if context:
                contexts.append(context)

        return "\n\n".join(contexts)
