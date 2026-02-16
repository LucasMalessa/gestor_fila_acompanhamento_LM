@echo off
REM Script para criar tarefa no Windows Task Scheduler
REM Executa main_lm.py todos os dias das 8h às 18h, a cada 1 hora

setlocal enabledelayedexpansion

echo.
echo ========================================
echo Criando Tarefa no Task Scheduler
echo ========================================
echo.

REM Caminho do projeto
set PROJECT_PATH=C:\Users\lmalessa\OneDrive - EDENRED\Gestor de Filas Acompanhamento LM
set PYTHON_EXE=C:\.venv\gestor_filas\Scripts\python.exe
set MAIN_SCRIPT=%PROJECT_PATH%\main_lm.py
set TASK_NAME=GestorFilasAcompanhamento

REM Removendo tarefa anterior se existir
echo [1/3] Removendo tarefa anterior (se existir)...
schtasks /delete /tn "%TASK_NAME%" /f >nul 2>&1

REM Criando a tarefa que executa a cada 1 hora entre 8h e 18h
echo [2/3] Criando nova tarefa...
schtasks /create /tn "%TASK_NAME%" ^
  /tr "\"!PYTHON_EXE!\" \"!MAIN_SCRIPT!\"" ^
  /sc daily ^
  /st 08:00:00 ^
  /du 11:00 ^
  /ri 60 ^
  /f

if errorlevel 1 (
    echo ERRO: Falha ao criar a tarefa
    pause
    exit /b 1
)

REM Verificando se a tarefa foi criada
echo [3/3] Verificando tarefa...
schtasks /query /tn "%TASK_NAME%" /v /fo list

echo.
echo ========================================
echo Tarefa criada com sucesso!
echo ========================================
echo.
echo Tarefa: %TASK_NAME%
echo Acao: Executar %MAIN_SCRIPT%
echo Frequencia: Diariamente das 08:00 às 18:00, a cada 1 hora
echo Diretorio: %PROJECT_PATH%
echo.
pause
