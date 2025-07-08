# 🧠 Assistente de Memória Avançado

Sistema de assistente pessoal com IA que registra, categoriza e gerencia eventos da sua vida através de voz.

## ✨ Funcionalidades

### 🎯 Categorização Inteligente
- **Trabalho** 💼 - Reuniões, prazos, projetos
- **Saúde** 🏥 - Consultas, exercícios, medicamentos
- **Pessoal** 👤 - Hobbies, metas pessoais
- **Família** 👨‍👩‍👧‍👦 - Eventos familiares, aniversários
- **Lazer** 🎮 - Entretenimento, viagens
- **Estudos** 📚 - Cursos, provas, leituras
- **Financeiro** 💰 - Contas, investimentos
- **Outros** 📌 - Eventos diversos

### 🔔 Sistema de Lembretes
- Notificações automáticas do sistema
- Configuração de lembretes por evento
- Suporte a diferentes intervalos (30min, 1h, 2h, 1 dia)

### 👥 Reconhecimento de Identidades
- Identifica pessoas mencionadas automaticamente
- Mantém contexto de relacionamentos
- Aprende preferências e detalhes

### 💾 Persistência Robusta
- Banco de dados SQLite
- Histórico completo de interações
- Backup automático de dados

### 🎤 Interface Natural
- Reconhecimento de voz em português
- Processamento com GPT-4o
- Comandos de voz para controle

## 🚀 Instalação

### 1. Clone o repositório
```bash
git clone <seu-repositorio>
cd agent-memory
```

### 2. Instale as dependências
```bash
pip install -r requirements_enhanced.txt
```

### 3. Configure as variáveis de ambiente
Crie um arquivo `.env` na pasta `agent-memory/`:
```
OPENAI_API_KEY=sua_chave_api_aqui
```

### 4. Execute o sistema
```bash
python main_enhanced.py
```

## 📖 Como Usar

### Comandos de Voz
- **"Sair"** - Encerra a aplicação
- **"Lembrar"** - Ativa modo de registro de eventos
- **"Consultar"** - Busca eventos salvos
- **"Identidade"** - Gerencia pessoas conhecidas

### Exemplos de Uso

#### Registrar Evento
```
"Tenho uma reunião de trabalho amanhã às 14h sobre o projeto novo"
```
**Resultado**: Evento categorizado como "Trabalho" com lembrete automático

#### Mencionar Pessoa
```
"Encontrei meu amigo João no shopping hoje"
```
**Resultado**: João é adicionado ao sistema como "amigo"

#### Consultar Eventos
```
"Quais são meus eventos de hoje?"
```
**Resultado**: Lista eventos do dia com categorização

## 🏗️ Estrutura do Projeto

```
agent-memory/
├── main_enhanced.py          # Sistema principal melhorado
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
└── gui/
    └── main_window.py        # Interface gráfica (opcional)
```

## 🔧 Configuração Avançada

### Banco de Dados
O sistema usa SQLite por padrão. Para usar outro banco:
1. Modifique `DatabaseManager` em `database/database.py`
2. Atualize a string de conexão

### Notificações
Para personalizar notificações:
1. Edite `ReminderSystem` em `notifications/reminder_system.py`
2. Configure intervalos e formatos

### Categorias
Para adicionar novas categorias:
1. Edite `EventCategory` em `tools/daily_events.py`
2. Adicione emoji correspondente no sistema

## 🐛 Solução de Problemas

### Erro de API Key
```
openai.RateLimitError: Error code: 429
```
**Solução**: Verifique sua conta OpenAI e adicione créditos

### Erro de Áudio
```
PermissionError: [WinError 32]
```
**Solução**: Aguarde alguns segundos e tente novamente

### Erro de Banco de Dados
```
sqlite3.OperationalError
```
**Solução**: Verifique permissões de escrita na pasta

## 📊 Recursos Técnicos

- **IA**: GPT-4o para processamento natural
- **Voz**: Whisper para transcrição
- **Banco**: SQLite para persistência
- **Notificações**: Plyer para sistema
- **Interface**: Tkinter (opcional)

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para detalhes.

## 🆘 Suporte

Para dúvidas ou problemas:
1. Verifique a documentação
2. Abra uma issue no GitHub
3. Consulte os logs de erro

---

**Desenvolvido com ❤️ para melhorar sua produtividade pessoal!** 
