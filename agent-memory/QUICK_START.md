# 🚀 Guia de Início Rápido - Assistente de Memória IA

## ⚡ Começando em 5 Minutos

### 1. **Instalação Rápida**
```bash
# Clone o projeto
git clone <seu-repositorio>
cd agent-memory

# Instale as dependências
pip install -r requirements_enhanced.txt

# Configure a API key
echo "OPENAI_API_KEY=sua_chave_aqui" > .env
```

### 2. **Configure sua API OpenAI**
1. Acesse: https://platform.openai.com/api-keys
2. Clique em "Create new secret key"
3. Copie a chave e cole no arquivo `.env`

### 3. **Execute o Sistema**
```bash
python main_enhanced.py
```

### 4. **Teste com Comandos de Voz**
```
"Tenho reunião de trabalho amanhã às 14h"
"Consulta médica na quinta-feira às 10h"
"Aniversário da minha mãe no próximo sábado"
"Sair"
```

---

## 🎯 Comandos Essenciais

### Comandos de Controle
- **"Sair"** - Encerra a aplicação
- **"Quit"** - Encerra a aplicação
- **"Exit"** - Encerra a aplicação

### Exemplos de Eventos
```
"Reunião de trabalho amanhã às 14h"
"Consulta médica na quinta às 10h"
"Aniversário da família no sábado"
"Prova de matemática na segunda"
"Conta de luz vence no dia 15"
```

### Exemplos de Pessoas
```
"Encontrei meu amigo João hoje"
"Reunião com a Maria sobre o projeto"
"Almoço com minha família no domingo"
```

---

## 📊 Categorias Disponíveis

| Categoria | Emoji | Exemplo |
|-----------|-------|---------|
| **Trabalho** | 💼 | "reunião de trabalho" |
| **Saúde** | 🏥 | "consulta médica" |
| **Pessoal** | 👤 | "hobby, meta pessoal" |
| **Família** | 👨‍👩‍👧‍👦 | "aniversário da família" |
| **Lazer** | 🎮 | "viagem, cinema" |
| **Estudos** | 📚 | "prova, curso" |
| **Financeiro** | 💰 | "conta, investimento" |
| **Outros** | 📌 | "evento diverso" |

---

## 🔔 Lembretes

### Formatos Suportados
```
"lembre-me 30min antes"
"lembre-me 1h antes"
"lembre-me 2h antes"
"lembre-me 1 dia antes"
```

### Exemplo Completo
```
"Tenho reunião amanhã às 14h, lembre-me 30min antes"
→ Lembrete configurado para 13:30 do dia seguinte
```

---

## 🐛 Problemas Comuns

### Erro: "No module named 'plyer'"
```bash
pip install plyer
```

### Erro: "openai.RateLimitError: Error code: 429"
- Adicione créditos na sua conta OpenAI
- Acesse: https://platform.openai.com/account/billing

### Erro: "PermissionError: [WinError 32]"
- Aguarde alguns segundos e tente novamente

### Erro: "ModuleNotFoundError"
```bash
pip install -r requirements_enhanced.txt
```

---

## 📈 Próximos Passos

### 1. **Explore as Funcionalidades**
- Teste diferentes categorias de eventos
- Experimente com lembretes
- Mencione pessoas para testar reconhecimento

### 2. **Personalize o Sistema**
- Adicione novas categorias em `tools/daily_events.py`
- Configure notificações em `notifications/reminder_system.py`
- Personalize o banco de dados em `database/database.py`

### 3. **Use a Interface Gráfica**
```bash
python gui/main_window.py
```

### 4. **Consulte a Documentação Completa**
- Leia `DOCUMENTATION.md` para detalhes técnicos
- Verifique `README_ENHANCED.md` para visão geral

---

## 🆘 Precisa de Ajuda?

### Recursos Disponíveis
- **Documentação Completa**: `DOCUMENTATION.md`
- **README**: `README_ENHANCED.md`
- **Logs**: Verifique a saída do console
- **Issues**: Abra uma issue no GitHub

### Contato
1. Verifique esta documentação
2. Consulte os logs de erro
3. Abra uma issue no GitHub

---

**🎉 Parabéns! Você está pronto para usar o Assistente de Memória IA!**

*Para mais informações, consulte a documentação completa em `DOCUMENTATION.md`* 
