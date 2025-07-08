# 📚 Documentação Completa - Assistente de Memória IA

## 🎯 Visão Geral

O **Assistente de Memória IA** é um sistema avançado de gerenciamento pessoal que utiliza inteligência artificial para registrar, categorizar e gerenciar eventos da sua vida através de comandos de voz em português.

### ✨ Principais Funcionalidades

- 🎤 **Reconhecimento de Voz** - Interface natural por voz
- 🧠 **IA Inteligente** - Processamento com GPT-4o
- 📊 **Categorização Automática** - 8 categorias de eventos
- 🔔 **Sistema de Lembretes** - Notificações automáticas
- 👥 **Reconhecimento de Identidades** - Contexto de pessoas
- 💾 **Persistência Robusta** - Banco de dados SQLite
- 🖥️ **Interface Gráfica** - GUI opcional com Tkinter

---

## 🏗️ Arquitetura do Sistema

### Estrutura de Diretórios
```
agent-memory/
├── main.py                    # Sistema básico (original)
├── main_enhanced.py           # Sistema avançado (melhorado)
├── database/
│   └── database.py           # Gerenciador de banco de dados
├── notifications/
│   └── reminder_system.py    # Sistema de lembretes
├── identity/
│   └── identity_manager.py   # Gerenciador de identidades
├── tools/
│   └── daily_events.py       # Modelos de eventos
├── utils/
│   ├── record_audio.py       # Gravação de áudio
│   └── basemodel2tool.py     # Conversão de modelos
├── gui/
│   └── main_window.py        # Interface gráfica
└── requirements_enhanced.txt  # Dependências
```

### Componentes Principais

#### 1. **Sistema Principal** (`main_enhanced.py`)
- **Classe**: `EnhancedMemoryAssistant`
- **Responsabilidade**: Orquestração do sistema completo
- **Funcionalidades**:
  - Processamento de áudio
  - Integração com IA
  - Gerenciamento de contexto
  - Salvamento de dados

#### 2. **Banco de Dados** (`database/database.py`)
- **Classe**: `DatabaseManager`
- **Responsabilidade**: Persistência de dados
- **Tabelas**:
  - `events` - Eventos categorizados
  - `interactions` - Histórico de conversas
  - `reminders` - Lembretes configurados
  - `identities` - Pessoas conhecidas

#### 3. **Sistema de Lembretes** (`notifications/reminder_system.py`)
- **Classe**: `ReminderSystem`
- **Responsabilidade**: Notificações automáticas
- **Funcionalidades**:
  - Thread em background
  - Notificações do sistema
  - Parsing de tempo de lembretes

#### 4. **Gerenciador de Identidades** (`identity/identity_manager.py`)
- **Classe**: `IdentityManager`
- **Responsabilidade**: Reconhecimento de pessoas
- **Funcionalidades**:
  - Extração automática de nomes
  - Contexto de relacionamentos
  - Filtros inteligentes

---

## 📊 Modelos de Dados

### Evento Individual (`Event`)
```python
class Event(BaseModel):
    title: str                    # Título do evento
    description: str              # Descrição detalhada
    category: EventCategory       # Categoria (trabalho, saúde, etc.)
    priority: EventPriority       # Prioridade (baixa, média, alta, urgente)
    time: Optional[str]          # Horário (HH:MM)
    location: Optional[str]       # Local do evento
    reminder: Optional[str]       # Lembrete (ex: "30min antes")
```

### Categorias de Eventos
```python
class EventCategory(str, Enum):
    TRABALHO = "trabalho"        # 💼 Reuniões, prazos, projetos
    SAUDE = "saude"              # 🏥 Consultas, exercícios, medicamentos
    PESSOAL = "pessoal"          # 👤 Hobbies, metas pessoais
    FAMILIA = "familia"          # 👨‍👩‍👧‍👦 Eventos familiares
    LAZER = "lazer"              # 🎮 Entretenimento, viagens
    ESTUDOS = "estudos"          # 📚 Cursos, provas, leituras
    FINANCEIRO = "financeiro"    # 💰 Contas, investimentos
    OUTROS = "outros"            # 📌 Eventos diversos
```

### Prioridades
```python
class EventPriority(str, Enum):
    BAIXA = "baixa"              # 🟢 Pouco urgente
    MEDIA = "media"              # 🟡 Importância normal
    ALTA = "alta"                # 🟠 Importante
    URGENTE = "urgente"          # 🔴 Muito urgente
```

---

## 🎤 Interface de Voz

### Comandos Suportados

#### Comandos de Controle
- **"Sair"** - Encerra a aplicação
- **"Quit"** - Encerra a aplicação
- **"Exit"** - Encerra a aplicação
- **"Encerrar"** - Encerra a aplicação
- **"Parar"** - Encerra a aplicação

#### Exemplos de Registro de Eventos
```
"Tenho uma reunião de trabalho amanhã às 14h sobre o projeto novo"
"Consulta médica na quinta-feira às 10h"
"Aniversário da minha mãe no próximo sábado"
"Prova de matemática na segunda-feira"
"Conta de luz vence no dia 15"
```

#### Exemplos de Mencionar Pessoas
```
"Encontrei meu amigo João no shopping hoje"
"Reunião com a Maria sobre o projeto"
"Almoço com minha família no domingo"
"Falei com o Pedro sobre o trabalho"
```

---

## 🔧 Configuração e Instalação

### 1. **Requisitos do Sistema**
- Python 3.8+
- Microfone funcional
- Conexão com internet (para API OpenAI)
- Espaço em disco: ~100MB

### 2. **Instalação**
```bash
# Clone o repositório
git clone <seu-repositorio>
cd agent-memory

# Instale as dependências
pip install -r requirements_enhanced.txt

# Configure a API key
echo "OPENAI_API_KEY=sua_chave_aqui" > .env
```

### 3. **Configuração da API OpenAI**
1. Acesse: https://platform.openai.com/api-keys
2. Crie uma nova API key
3. Adicione no arquivo `.env`:
   ```
   OPENAI_API_KEY=sk-...
   ```

### 4. **Execução**
```bash
# Sistema básico
python main.py

# Sistema avançado (recomendado)
python main_enhanced.py
```

---

## 🗄️ Banco de Dados

### Estrutura das Tabelas

#### Tabela `events`
```sql
CREATE TABLE events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,           -- Data do evento
    title TEXT NOT NULL,          -- Título
    description TEXT,             -- Descrição
    category TEXT NOT NULL,       -- Categoria
    priority TEXT DEFAULT 'media', -- Prioridade
    time TEXT,                    -- Horário
    location TEXT,                -- Local
    reminder TEXT,                -- Lembrete
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### Tabela `interactions`
```sql
CREATE TABLE interactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    human_message TEXT,           -- Mensagem do usuário
    assistant_message TEXT,       -- Resposta da IA
    context TEXT                  -- Contexto adicional
);
```

#### Tabela `reminders`
```sql
CREATE TABLE reminders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_id INTEGER,             -- Referência ao evento
    reminder_time TIMESTAMP,      -- Quando enviar
    message TEXT,                 -- Mensagem do lembrete
    is_sent BOOLEAN DEFAULT FALSE, -- Se já foi enviado
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (event_id) REFERENCES events (id)
);
```

#### Tabela `identities`
```sql
CREATE TABLE identities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,           -- Nome da pessoa
    role TEXT,                    -- Função/cargo
    relationship TEXT,            -- Relacionamento
    preferences TEXT,             -- Preferências
    notes TEXT,                   -- Notas adicionais
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## 🔔 Sistema de Lembretes

### Funcionalidades
- **Thread em Background** - Verifica lembretes a cada minuto
- **Notificações do Sistema** - Usa plyer para notificações nativas
- **Fallback para Console** - Se plyer não estiver disponível
- **Parsing Inteligente** - Converte texto em timestamps

### Formatos de Lembrete Suportados
```
"30min antes"     → 30 minutos antes do evento
"1h antes"        → 1 hora antes do evento
"2h antes"        → 2 horas antes do evento
"1 dia antes"     → 1 dia antes do evento
"1d antes"        → 1 dia antes do evento
```

### Exemplo de Uso
```
"Tenho reunião amanhã às 14h, lembre-me 30min antes"
→ Lembrete configurado para 13:30 do dia seguinte
```

---

## 👥 Reconhecimento de Identidades

### Padrões Reconhecidos
```python
# Padrões suportados:
"meu amigo João"              → João (amigo)
"minha irmã Maria"            → Maria (irmã)
"João é meu colega"           → João (colega)
"reunião com Pedro"           → Pedro (reconhecido)
"almoço com a família"        → família (reconhecida)
```

### Filtros Inteligentes
O sistema filtra automaticamente:
- Verbos comuns (estive, fui, vou, etc.)
- Palavras temporais (ontem, hoje, amanhã)
- Pronomes e artigos
- Palavras de ação (trabalho, estudo, etc.)

### Contexto Mantido
Para cada pessoa reconhecida, o sistema mantém:
- **Nome** - Como foi mencionado
- **Relacionamento** - Amigo, família, colega, etc.
- **Preferências** - Informações aprendidas
- **Notas** - Observações adicionais

---

## 🖥️ Interface Gráfica

### Funcionalidades da GUI
- **Área de Chat** - Histórico de conversas
- **Display de Eventos** - Eventos do dia atual
- **Botões de Controle** - Gravar, parar, limpar
- **Status Bar** - Informações do sistema
- **Threading** - Interface responsiva

### Como Usar a GUI
1. Execute `python gui/main_window.py`
2. Clique em "🎤 Gravar Áudio"
3. Fale seu comando
4. Clique em "⏹️ Parar"
5. Veja a resposta processada

---

## 🔧 Configuração Avançada

### Personalização de Categorias
```python
# Em tools/daily_events.py
class EventCategory(str, Enum):
    # Adicione novas categorias aqui
    NOVA_CATEGORIA = "nova_categoria"
```

### Configuração de Notificações
```python
# Em notifications/reminder_system.py
def _send_notification(self, title, message, event_time, event_date):
    # Personalize o formato das notificações
    notification_title = f"🔔 {title}"
    notification_message = f"{message}\nData: {event_date}"
```

### Banco de Dados Personalizado
```python
# Em database/database.py
class DatabaseManager:
    def __init__(self, db_path: str = "seu_banco.db"):
        # Use um banco diferente
        self.db_path = db_path
```

---

## 🐛 Solução de Problemas

### Erro: "No module named 'plyer'"
```bash
pip install plyer
```

### Erro: "openai.RateLimitError: Error code: 429"
- Verifique sua conta OpenAI
- Adicione créditos ou método de pagamento
- Acesse: https://platform.openai.com/account/billing

### Erro: "PermissionError: [WinError 32]"
- Aguarde alguns segundos e tente novamente
- O arquivo de áudio ainda está sendo usado

### Erro: "sqlite3.OperationalError"
- Verifique permissões de escrita na pasta
- Certifique-se de que o SQLite está funcionando

### Erro: "ModuleNotFoundError"
```bash
# Instale todas as dependências
pip install -r requirements_enhanced.txt
```

---

## 📈 Melhorias Futuras

### Funcionalidades Planejadas
- [ ] **Sincronização em Nuvem** - Backup automático
- [ ] **API REST** - Interface web
- [ ] **Múltiplos Idiomas** - Suporte a inglês, espanhol
- [ ] **Integração com Calendário** - Google Calendar, Outlook
- [ ] **Análise de Sentimento** - Detecção de humor
- [ ] **Relatórios** - Estatísticas de eventos
- [ ] **Backup Automático** - Exportação de dados
- [ ] **Modo Offline** - Funcionamento sem internet

### Otimizações Técnicas
- [ ] **Cache Inteligente** - Reduzir chamadas à API
- [ ] **Compressão de Áudio** - Menor uso de banda
- [ ] **Indexação de Banco** - Consultas mais rápidas
- [ ] **Logs Estruturados** - Melhor debugging
- [ ] **Testes Automatizados** - Cobertura de código

---

## 📄 Licença e Contribuição

### Licença
Este projeto está sob a licença MIT.

### Como Contribuir
1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

### Padrões de Código
- Use type hints em todas as funções
- Documente funções complexas
- Siga PEP 8 para formatação
- Teste suas mudanças

---

## 🆘 Suporte

### Recursos de Ajuda
- **Documentação**: Este arquivo
- **Issues**: GitHub Issues
- **Logs**: Verifique a saída do console
- **Debug**: Use `print()` para debugging

### Contato
Para dúvidas ou problemas:
1. Verifique esta documentação
2. Consulte os logs de erro
3. Abra uma issue no GitHub
4. Verifique a documentação da OpenAI

---

**Desenvolvido com ❤️ para melhorar sua produtividade pessoal!**

*Última atualização: Janeiro 2025* 
