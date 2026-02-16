@echo off
REM Script para configurar o Virtual Environment para o projeto
REM Este script cria um venv em C:\.venv\gestor_filas

echo.
echo ========================================
echo Configurando Virtual Environment
echo ========================================
echo.

REM Verificar se Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ERRO: Python não está instalado ou não está no PATH
    pause
    exit /b 1
)

echo [1/3] Criando diretório C:\.venv...
if not exist "C:\.venv" mkdir "C:\.venv"

echo [2/3] Criando Virtual Environment em C:\.venv\gestor_filas...
python -m venv "C:\.venv\gestor_filas"

if errorlevel 1 (
    echo ERRO: Falha ao criar o Virtual Environment
    pause
    exit /b 1
)

echo [3/3] Instalando dependências...
cd /d "%~dp0"
"C:\.venv\gestor_filas\Scripts\python.exe" -m pip install --upgrade pip
"C:\.venv\gestor_filas\Scripts\python.exe" -m pip install -r requirements.txt

echo.
echo ========================================
echo Setup concluído com sucesso!
echo ========================================
echo.
echo Virtual Environment está em: C:\.venv\gestor_filas
echo Python executável: C:\.venv\gestor_filas\Scripts\python.exe
echo.
pause
