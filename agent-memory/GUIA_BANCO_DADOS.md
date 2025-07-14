# 🗄️ Guia do Banco de Dados

## 📋 Sobre o Banco de Dados

O projeto usa **SQLite** como banco de dados, que é um banco de dados local e não requer instalação de servidor. O arquivo do banco é `memory.db` na pasta `agent-memory/`.

### ✅ **Vantagens do SQLite:**
- ✅ Não precisa de servidor
- ✅ Arquivo único e portável
- ✅ Funciona offline
- ✅ Fácil de fazer backup
- ✅ Não precisa de configuração

### ❌ **Desvantagens:**
- ❌ Não é adequado para múltiplos usuários simultâneos
- ❌ Não tem interface gráfica nativa
- ❌ Limitações de performance para grandes volumes

## 🗂️ Estrutura do Banco

### Tabelas Criadas:

1. **`events`** - Eventos e compromissos
   - `id` - Identificador único
   - `date` - Data do evento
   - `title` - Título do evento
   - `description` - Descrição detalhada
   - `category` - Categoria (trabalho, saude, pessoal, etc.)
   - `priority` - Prioridade (baixa, media, alta, urgente)
   - `time` - Horário (opcional)
   - `location` - Local (opcional)
   - `reminder` - Lembrete (opcional)
   - `created_at` - Data de criação
   - `updated_at` - Data de atualização

2. **`interactions`** - Histórico de conversas
   - `id` - Identificador único
   - `timestamp` - Data/hora da interação
   - `human_message` - Mensagem do usuário
   - `assistant_message` - Resposta do assistente
   - `context` - Contexto adicional

3. **`reminders`** - Sistema de lembretes
   - `id` - Identificador único
   - `event_id` - Referência ao evento
   - `reminder_time` - Horário do lembrete
   - `message` - Mensagem do lembrete
   - `is_sent` - Se foi enviado
   - `created_at` - Data de criação

4. **`identities`** - Pessoas conhecidas
   - `id` - Identificador único
   - `name` - Nome da pessoa
   - `role` - Papel/função
   - `relationship` - Relacionamento
   - `preferences` - Preferências
   - `notes` - Notas adicionais
   - `created_at` - Data de criação
   - `updated_at` - Data de atualização

## 🔍 Como Verificar se os Dados Estão Sendo Salvos

### 1. **Usando o Script de Visualização**
```bash
cd agent-memory
python view_database.py
```

Este script vai mostrar:
- ✅ Todos os eventos salvos
- ✅ Interações recentes
- ✅ Lembretes configurados
- ✅ Identidades reconhecidas
- ✅ Estatísticas gerais

### 2. **Verificando o Arquivo do Banco**
```bash
# Verificar se o arquivo existe
ls -la memory.db

# Verificar o tamanho do arquivo
du -h memory.db
```

### 3. **Usando SQLite Browser (Interface Gráfica)**

Se quiser uma interface gráfica, você pode usar:

**Windows:**
- [DB Browser for SQLite](https://sqlitebrowser.org/)
- [DBeaver](https://dbeaver.io/)

**Instalação:**
1. Baixe e instale o DB Browser for SQLite
2. Abra o arquivo `memory.db`
3. Navegue pelas tabelas na aba "Browse Data"

## 🔄 Migração para MySQL/PostgreSQL

Se você quiser usar MySQL ou PostgreSQL:

### **Para MySQL:**

1. **Instale o MySQL:**
   ```bash
   # Windows (usando XAMPP ou similar)
   # Ou instale MySQL Server diretamente
   ```

2. **Crie o banco:**
   ```sql
   CREATE DATABASE agent_memory;
   USE agent_memory;
   ```

3. **Modifique o código:**
   ```python
   # Em database/database.py
   import mysql.connector
   
   class DatabaseManager:
       def __init__(self):
           self.connection = mysql.connector.connect(
               host="localhost",
               user="seu_usuario",
               password="sua_senha",
               database="agent_memory"
           )
   ```

### **Para PostgreSQL:**

1. **Instale o PostgreSQL:**
   ```bash
   # Windows: Baixe do site oficial
   # https://www.postgresql.org/download/windows/
   ```

2. **Crie o banco:**
   ```sql
   CREATE DATABASE agent_memory;
   ```

3. **Modifique o código:**
   ```python
   # Em database/database.py
   import psycopg2
   
   class DatabaseManager:
       def __init__(self):
           self.connection = psycopg2.connect(
               host="localhost",
               database="agent_memory",
               user="seu_usuario",
               password="sua_senha"
           )
   ```

## 📊 Ferramentas de Visualização

### **1. DB Browser for SQLite (Recomendado)**
- Interface gráfica completa
- Permite editar dados
- Exportar para CSV/JSON
- Executar queries SQL

### **2. DBeaver (Universal)**
- Suporta múltiplos bancos
- Interface moderna
- Bom para desenvolvimento

### **3. phpMyAdmin (MySQL)**
- Interface web para MySQL
- Fácil de usar
- Bom para administração

### **4. pgAdmin (PostgreSQL)**
- Interface oficial do PostgreSQL
- Recursos avançados
- Bom para administração

## 🛠️ Comandos Úteis

### **Verificar se o banco está funcionando:**
```bash
cd agent-memory
python view_database.py
```

### **Fazer backup do banco:**
```bash
cp memory.db memory_backup_$(date +%Y%m%d).db
```

### **Exportar dados para JSON:**
```bash
python view_database.py
# Escolha 's' quando perguntado sobre exportar
```

### **Verificar tamanho do banco:**
```bash
du -h memory.db
```

## 🔧 Troubleshooting

### **Problema: "database is locked"**
**Solução:** Feche todas as conexões com o banco e tente novamente.

### **Problema: "no such table"**
**Solução:** O banco não foi inicializado. Execute o programa uma vez para criar as tabelas.

### **Problema: "permission denied"**
**Solução:** Verifique as permissões da pasta onde está o arquivo `memory.db`.

### **Problema: Banco corrompido**
**Solução:** 
1. Faça backup do arquivo atual
2. Delete o arquivo `memory.db`
3. Execute o programa novamente para recriar

## 📈 Monitoramento

Para monitorar se os dados estão sendo salvos:

1. **Execute o programa e registre alguns eventos**
2. **Execute o visualizador:**
   ```bash
   python view_database.py
   ```
3. **Verifique se aparecem os eventos registrados**

Se os eventos aparecerem na visualização, significa que o banco está funcionando corretamente! ✅ 
