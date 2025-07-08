# 📖 Referência da API - Assistente de Memória IA

## 🏗️ Estrutura das Classes

### EnhancedMemoryAssistant

**Arquivo**: `main_enhanced.py`

**Responsabilidade**: Classe principal que orquestra todo o sistema.

#### Métodos Principais

```python
class EnhancedMemoryAssistant:
    def __init__(self) -> None
    """Inicializa o assistente com todos os componentes."""
    
    def process_audio(self, filename_audio: str) -> str
    """Processa áudio e retorna transcrição."""
    
    def extract_identities(self, text: str) -> List[Dict[str, Any]]
    """Extrai identidades do texto."""
    
    def get_context(self) -> Dict[str, Any]
    """Obtém contexto completo da memória."""
    
    def process_with_ai(self, text: str, context: Dict[str, Any]) -> Optional[Dict[str, Any]]
    """Processa texto com IA usando contexto completo."""
    
    def save_events(self, events_data: Dict[str, Any]) -> bool
    """Salva eventos no banco de dados."""
    
    def save_interaction(self, human_message: str, assistant_message: str) -> None
    """Salva interação no banco de dados."""
    
    def run(self) -> None
    """Executa o loop principal do assistente."""
```

---

### DatabaseManager

**Arquivo**: `database/database.py`

**Responsabilidade**: Gerenciamento de persistência de dados.

#### Métodos Principais

```python
class DatabaseManager:
    def __init__(self, db_path: str = "memory.db") -> None
    """Inicializa o gerenciador de banco de dados."""
    
    def init_database(self) -> None
    """Inicializa o banco de dados com as tabelas necessárias."""
    
    def save_events(self, events_data: Dict[str, Any]) -> bool
    """Salva eventos no banco de dados."""
    
    def save_interaction(self, human_message: str, assistant_message: str, context: str = "") -> None
    """Salva uma interação no banco de dados."""
    
    def get_events_by_date(self, date: str) -> List[Dict[str, Any]]
    """Busca eventos por data."""
    
    def get_recent_interactions(self, limit: int = 10) -> List[Dict[str, Any]]
    """Busca interações recentes."""
    
    def get_memory_context(self) -> Dict[str, Any]
    """Retorna contexto completo da memória."""
```

#### Estrutura do Banco

```sql
-- Tabela de eventos
CREATE TABLE events (
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
);

-- Tabela de interações
CREATE TABLE interactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    human_message TEXT,
    assistant_message TEXT,
    context TEXT
);

-- Tabela de lembretes
CREATE TABLE reminders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_id INTEGER,
    reminder_time TIMESTAMP,
    message TEXT,
    is_sent BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (event_id) REFERENCES events (id)
);

-- Tabela de identidades
CREATE TABLE identities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    role TEXT,
    relationship TEXT,
    preferences TEXT,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

### ReminderSystem

**Arquivo**: `notifications/reminder_system.py`

**Responsabilidade**: Sistema de lembretes e notificações.

#### Métodos Principais

```python
class ReminderSystem:
    def __init__(self, db_path: str = "memory.db") -> None
    """Inicializa o sistema de lembretes."""
    
    def start(self) -> None
    """Inicia o sistema de lembretes em background."""
    
    def stop(self) -> None
    """Para o sistema de lembretes."""
    
    def create_reminder(self, event_id: int, reminder_time: str, message: str) -> None
    """Cria um novo lembrete."""
    
    def parse_reminder_time(self, reminder_text: str, event_date: str, event_time: Optional[str] = None) -> str
    """Converte texto de lembrete em timestamp."""
```

#### Formatos de Lembrete Suportados

```python
# Formatos reconhecidos:
"30min antes"     → 30 minutos antes do evento
"30 minutos antes" → 30 minutos antes do evento
"1h antes"        → 1 hora antes do evento
"1 hora antes"    → 1 hora antes do evento
"2h antes"        → 2 horas antes do evento
"2 horas antes"   → 2 horas antes do evento
"1 dia antes"     → 1 dia antes do evento
"1d antes"        → 1 dia antes do evento
```

---

### IdentityManager

**Arquivo**: `identity/identity_manager.py`

**Responsabilidade**: Reconhecimento e gerenciamento de identidades.

#### Métodos Principais

```python
class IdentityManager:
    def __init__(self, db_path: str = "memory.db") -> None
    """Inicializa o gerenciador de identidades."""
    
    def add_identity(self, name: str, role: Optional[str] = None, relationship: Optional[str] = None, 
                    preferences: Optional[str] = None, notes: Optional[str] = None) -> bool
    """Adiciona uma nova identidade."""
    
    def get_identity(self, name: str) -> Optional[Dict[str, Any]]
    """Busca uma identidade por nome."""
    
    def update_identity(self, name: str, **kwargs: Any) -> bool
    """Atualiza uma identidade existente."""
    
    def get_all_identities(self) -> List[Dict[str, Any]]
    """Retorna todas as identidades."""
    
    def extract_identities_from_text(self, text: str) -> List[Dict[str, Any]]
    """Extrai informações de identidade do texto."""
    
    def get_context_for_identity(self, name: str) -> str
    """Retorna contexto para uma identidade específica."""
    
    def get_all_contexts(self) -> str
    """Retorna contexto de todas as identidades."""
```

#### Padrões de Reconhecimento

```python
# Padrões suportados:
r'(?:meu|minha)\s+(?:amigo|amiga|irmão|irmã|pai|mãe|filho|filha|marido|esposa|namorado|namorada|colega|vizinho|professor|médico)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)'
r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+(?:é|é meu|é minha)\s+(amigo|amiga|irmão|irmã|pai|mãe|filho|filha|marido|esposa|namorado|namorada)'
r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+(?:trabalha|estuda|mora|gosta|prefere|está|foi|vai)\s+'
r'(?:conheci|encontrei|falei com|visitei|chamei)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)'
r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+(?:disse|falou|mencionou|contou|explicou)'
r'(?:reunião|almoço|jantar|encontro|conversa)\s+(?:com|entre)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)'
```

---

### MemoryAssistantGUI

**Arquivo**: `gui/main_window.py`

**Responsabilidade**: Interface gráfica do sistema.

#### Métodos Principais

```python
class MemoryAssistantGUI:
    def __init__(self, db_manager, reminder_system) -> None
    """Inicializa a interface gráfica."""
    
    def setup_ui(self) -> None
    """Configura a interface do usuário."""
    
    def start_recording(self) -> None
    """Inicia gravação de áudio."""
    
    def stop_recording(self) -> None
    """Para gravação de áudio."""
    
    def process_audio(self, audio_text: str) -> None
    """Processa áudio gravado."""
    
    def add_message(self, sender: str, message: str, msg_type: str = "normal") -> None
    """Adiciona mensagem à área de chat."""
    
    def update_events_display(self) -> None
    """Atualiza display de eventos."""
    
    def run(self) -> None
    """Executa a interface gráfica."""
```

---

## 📊 Modelos de Dados

### Event

```python
class Event(BaseModel):
    title: str = Field(description="Título do evento")
    description: str = Field(description="Descrição detalhada do evento")
    category: EventCategory = Field(default=EventCategory.OUTROS, description="Categoria do evento")
    priority: EventPriority = Field(default=EventPriority.MEDIA, description="Prioridade do evento")
    time: Optional[str] = Field(default=None, description="Horário do evento (HH:MM)")
    location: Optional[str] = Field(default=None, description="Local do evento")
    reminder: Optional[str] = Field(default=None, description="Lembrete (ex: 30min antes)")
```

### EventCategory

```python
class EventCategory(str, Enum):
    TRABALHO = "trabalho"        # 💼
    SAUDE = "saude"              # 🏥
    PESSOAL = "pessoal"          # 👤
    FAMILIA = "familia"          # 👨‍👩‍👧‍👦
    LAZER = "lazer"              # 🎮
    ESTUDOS = "estudos"          # 📚
    FINANCEIRO = "financeiro"    # 💰
    OUTROS = "outros"            # 📌
```

### EventPriority

```python
class EventPriority(str, Enum):
    BAIXA = "baixa"              # 🟢
    MEDIA = "media"              # 🟡
    ALTA = "alta"                # 🟠
    URGENTE = "urgente"          # 🔴
```

### DailyEvents

```python
class DailyEvents(BaseModel):
    date: str = Field(description="Data em que os eventos ocorreram no formato DD/MM/YYYY")
    events: List[Event] = Field(description="Lista de eventos identificados no dia com categorização")
```

---

## 🔧 Configuração

### Variáveis de Ambiente

```bash
# Arquivo .env
OPENAI_API_KEY=sua_chave_api_aqui
```

### Dependências

```bash
# requirements_enhanced.txt
openai>=1.0.0
python-dotenv>=1.0.0
pydantic>=2.0.0
plyer>=2.1.0
```

---

## 🎯 Exemplos de Uso

### Inicialização Básica

```python
from main_enhanced import EnhancedMemoryAssistant

# Cria e executa o assistente
assistant = EnhancedMemoryAssistant()
assistant.run()
```

### Uso do Banco de Dados

```python
from database.database import DatabaseManager

# Inicializa o banco
db = DatabaseManager("meu_banco.db")

# Salva eventos
events_data = {
    'date': '15/01/2025',
    'events': [
        {
            'title': 'Reunião de trabalho',
            'description': 'Discussão sobre o projeto',
            'category': 'trabalho',
            'priority': 'alta',
            'time': '14:00',
            'location': 'Sala de reuniões'
        }
    ]
}
db.save_events(events_data)

# Busca eventos
events = db.get_events_by_date('15/01/2025')
```

### Uso do Sistema de Lembretes

```python
from notifications.reminder_system import ReminderSystem

# Inicializa o sistema
reminder_system = ReminderSystem()

# Inicia o sistema em background
reminder_system.start()

# Cria um lembrete
reminder_system.create_reminder(
    event_id=1,
    reminder_time="2025-01-15 13:30:00",
    message="Lembrete: Reunião em 30 minutos"
)

# Para o sistema
reminder_system.stop()
```

### Uso do Gerenciador de Identidades

```python
from identity.identity_manager import IdentityManager

# Inicializa o gerenciador
identity_manager = IdentityManager()

# Adiciona uma identidade
identity_manager.add_identity(
    name="João Silva",
    relationship="amigo",
    preferences="Gosta de futebol"
)

# Extrai identidades do texto
text = "Encontrei meu amigo João no shopping hoje"
identities = identity_manager.extract_identities_from_text(text)

# Obtém contexto
context = identity_manager.get_context_for_identity("João")
```

---

## 🐛 Tratamento de Erros

### Erros Comuns e Soluções

```python
# Erro de API OpenAI
try:
    completion = client.chat.completions.create(...)
except openai.RateLimitError:
    print("Erro: Limite de quota atingido")
    # Adicione créditos na conta OpenAI

# Erro de arquivo de áudio
try:
    os.remove(filename_audio)
except PermissionError:
    print("Arquivo ainda em uso, aguarde...")
    time.sleep(1)
    # Tenta novamente

# Erro de banco de dados
try:
    conn = sqlite3.connect(db_path)
except sqlite3.OperationalError:
    print("Erro de permissão no banco de dados")
    # Verifique permissões de escrita
```

---

## 📈 Extensibilidade

### Adicionando Novas Categorias

```python
# Em tools/daily_events.py
class EventCategory(str, Enum):
    # Categorias existentes...
    NOVA_CATEGORIA = "nova_categoria"

# Adicione o emoji correspondente
def get_category_emoji(self, category: str) -> str:
    emojis = {
        # Emojis existentes...
        'nova_categoria': '🆕'
    }
    return emojis.get(category, '📌')
```

### Personalizando Notificações

```python
# Em notifications/reminder_system.py
def _send_notification(self, title: str, message: str, event_time: Optional[str], event_date: str) -> None:
    # Personalize o formato
    notification_title = f"🔔 {title}"
    notification_message = f"{message}\nData: {event_date}"
    
    # Adicione lógica personalizada
    if "urgente" in message.lower():
        notification_title = f"🚨 URGENTE: {title}"
```

---

**📖 Para mais detalhes, consulte a documentação completa em `DOCUMENTATION.md`** 
