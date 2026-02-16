# 🚀 Guia de Setup - Gestor de Filas Acompanhamento LM

Este documento descreve como configurar o projeto em um novo computador ou ambiente.

---

## 1️⃣ Pré-requisitos

- **Windows 10/11** com PowerShell
- **Python 3.x** instalado e acessível via linha de comando
- **Acesso ao OneDrive/SharePoint** com a pasta `OneDrive - EDENRED` sincronizada
- Pasta `Fichiers de Usuario Servicio Telemetria JBS - Dados Acompanhamento` (contendo `relatorioAcompanhamento.csv`)

### Verificar Python
```powershell
python --version
```

---

## 2️⃣ Passo 1: Configurar Virtual Environment

### Opção A: Automático (Recomendado)
Execute o script de setup no diretório do projeto:
```batch
setup_venv.bat
```

Este script irá:
- ✅ Criar `C:\.venv\gestor_filas` (fora do OneDrive)
- ✅ Instalar dependências: `pandas`, `numpy`, `openpyxl`, `watchdog`

### Opção B: Manual
```powershell
# Criar venv
python -m venv C:\.venv\gestor_filas

# Ativar (se necessário)
C:\.venv\gestor_filas\Scripts\Activate.ps1

# Instalar dependências
C:\.venv\gestor_filas\Scripts\python.exe -m pip install -r requirements.txt
```

---

## 3️⃣ Passo 2: Configurar Task Scheduler

### Opção A: Automático (Recomendado)
Execute o script no diretório do projeto:
```batch
setup_task_scheduler.bat
```

Este script irá:
- ✅ Criar tarefa `GestorFilasAcompanhamento`
- ✅ Configurar execução diária das 08:00 às 18:00, a cada 1 hora
- ✅ Usar o Python do venv para executar `main_lm.py`

### Opção B: Manual
1. Abra **Task Scheduler**: `Win + R` → Digite `taskschd.msc` → Enter
2. Clique em **Ação** → **Criar Tarefa Básica...**
3. Preencha:
   - **Nome**: `GestorFilasAcompanhamento`
   - **Descrição**: `Executa análise de filas de acompanhamento de manutenção`
4. **Gatilho**:
   - Tipo: **Diariamente**
   - Hora: **08:00**
5. **Ação**:
   - Programa: `C:\.venv\gestor_filas\Scripts\python.exe`
   - Argumentos: `C:\Users\{SEU_USUARIO}\OneDrive - EDENRED\Gestor de Filas Acompanhamento LM\main_lm.py`
   - Iniciar em: `C:\Users\{SEU_USUARIO}\OneDrive - EDENRED\Gestor de Filas Acompanhamento LM`
6. **Condições**:
   - Desmarque: "Parar a tarefa se ela executar por mais de X horas"
7. **Configurações**:
   - Marque: "Se a tarefa estiver em execução quando chegar a hora de ocorrência, inicie uma nova instância conforme necessário"
   - Repita: **A cada 1 hora**
   - Duração: **11 horas**

---

## 4️⃣ Verificar Configuração

### Listar Tarefa
```powershell
Get-ScheduledTask -TaskName "GestorFilasAcompanhamento" | Select-Object TaskName, State, Description
```

### Ver Detalhes
```powershell
Get-ScheduledTask -TaskName "GestorFilasAcompanhamento" | Get-ScheduledTaskInfo
```

### Executar Manualmente (para teste)
```powershell
Start-ScheduledTask -TaskName "GestorFilasAcompanhamento"
```

### Ver Histórico
```powershell
Get-WinEvent -LogName "Microsoft-Windows-TaskScheduler/Operational" | Where-Object {$_.Properties[0].Value -eq "GestorFilasAcompanhamento"} | Format-List
```

---

## 5️⃣ Estrutura de Diretórios

Após setup, a estrutura fica assim:

```
C:\.venv\
└── gestor_filas\                           ← Virtual Environment (FORA do OneDrive)
    ├── Scripts\
    │   ├── python.exe                      ← Python executável
    │   └── pip.exe
    ├── Lib\
    └── ...

C:\Users\{SEU_USUARIO}\
└── OneDrive - EDENRED\
    ├── Gestor de Filas Acompanhamento LM\  ← Projeto (NO OneDrive)
    │   ├── main_lm.py                      ← Script principal
    │   ├── atualizador.py                  ← Monitor de arquivo
    │   ├── main_lm.exe                     ← Executável compilado
    │   ├── setup_venv.bat                  ← Setup automático do venv
    │   ├── setup_task_scheduler.bat        ← Setup automático do Task Scheduler
    │   ├── requirements.txt                ← Dependências Python
    │   ├── .env                            ← Configurações (não commitado)
    │   ├── .gitignore
    │   ├── README.md
    │   ├── SETUP.md                        ← Este arquivo
    │   └── ...arquivos de dados...
    │
    └── Dados Acompanhamento\
        └── relatorioAcompanhamento.csv     ← Fonte de dados (atualiza a cada 1h)
```

---

## 6️⃣ Cenários Comuns

### Cenário: Reinstalar dependências
```powershell
C:\.venv\gestor_filas\Scripts\python.exe -m pip install --upgrade -r requirements.txt
```

### Cenário: O venv foi deletado acidentalmente
Execute novamente:
```batch
setup_venv.bat
```

### Cenário: Mudar horário ou frequência da tarefa
1. Abra Task Scheduler: `taskschd.msc`
2. Localize `GestorFilasAcompanhamento`
3. Clique com direito → **Propriedades** → **Gatilhos**
4. Edite conforme necessário

### Cenário: Desabilitar/Habilitar a tarefa
```powershell
# Desabilitar
Disable-ScheduledTask -TaskName "GestorFilasAcompanhamento"

# Habilitar
Enable-ScheduledTask -TaskName "GestorFilasAcompanhamento"
```

### Cenário: Deletar tarefa
```powershell
Unregister-ScheduledTask -TaskName "GestorFilasAcompanhamento" -Confirm:$false
```

---

## 7️⃣ Troubleshooting

### Erro: "Python não encontrado"
Certifique-se de que Python está no PATH:
```powershell
python --version
```

Se não funcionar, reinstale Python ou use o caminho completo para o executável do venv.

### Erro: "relatorioAcompanhamento.csv não encontrado"
Verifique se:
1. A pasta do OneDrive está sincronizada
2. O arquivo existe em: `C:\Users\{SEU_USUARIO}\OneDrive - EDENRED\Dados Acompanhamento\relatorioAcompanhamento.csv`
3. Execute manualmente para ver o erro específico:
   ```powershell
   C:\.venv\gestor_filas\Scripts\python.exe C:\Users\{SEU_USUARIO}\OneDrive...\main_lm.py
   ```

### Erro: "Acesso negado" no Task Scheduler
Execute o PowerShell como Administrador antes de rodar `setup_task_scheduler.bat`.

### Task não está executando
1. Verifique se está habilitada:
   ```powershell
   Get-ScheduledTask -TaskName "GestorFilasAcompanhamento" | Select-Object State
   ```
2. Verifique o último status:
   ```powershell
   Get-ScheduledTask -TaskName "GestorFilasAcompanhamento" | Get-ScheduledTaskInfo
   ```
3. Força uma execução manual:
   ```powershell
   Start-ScheduledTask -TaskName "GestorFilasAcompanhamento"
   ```

---

## 8️⃣ Próximos Passos

✅ Setup concluído! Agora:

1. **Verifique os logs** da primeira execução:
   - Pasta: `C:\Users\{SEU_USUARIO}\OneDrive - EDENRED\Gestor de Filas Acompanhamento LM\arquivos_painel\`
   - Arquivo: `protocolos_agente.csv` (deve ser gerado a cada execução)

2. **Configure o Power BI** para conectar em:
   - `C:\Users\{SEU_USUARIO}\OneDrive - EDENRED\Gestor de Filas Acompanhamento LM\arquivos_painel\protocolos_agente.csv`
   - Este arquivo é atualizado a cada execução da tarefa

3. **Monitore execuções** via Task Scheduler:
   - Abra: `taskschd.msc`
   - Navegue até: `Task Scheduler Library`
   - Procure: `GestorFilasAcompanhamento`
   - Clique em: "Histórico" (aba)

---

**Data de criação**: 16/02/2026  
**Versão**: 1.0
