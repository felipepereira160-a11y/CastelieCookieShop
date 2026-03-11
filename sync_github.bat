@echo off
setlocal
cd /d "%~dp0"

if not exist .git (
  echo ERRO: Este script deve ser executado na pasta do repositorio.
  pause
  exit /b 1
)

echo === Sincronizando com GitHub (descartando alteracoes locais) ===
git fetch origin
if errorlevel 1 goto :error

git reset --hard origin/main
if errorlevel 1 goto :error

echo OK: repositorio alinhado com o GitHub.
pause
exit /b 0

:error
echo ERRO: falha ao sincronizar.
pause
exit /b 1
